import asyncio
import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import settings
from db.crud.user_crud import UserCrud
from notion.notion_api import notion_client
from openai_api.api import openai_client, update_assistant
from utils import get_notion_db_id

# from aiogram.fsm.context import FSMContext
# from states.user_states import UserStates


router = Router()


@router.message(CommandStart())
async def get_start(message: Message):
    """Регистрируем юзера"""
    if not await UserCrud.get_user_id(message.from_user.id):
        await UserCrud.create_user(user_id=message.from_user.id)
        await message.answer('Вы были успешно зарегистрированы!✅\nТеперь введите ссылку на вашу базу данных из Notion')
    else:
        await message.answer('Вы уже зарегестрированы')


@router.message(F.text.regexp(r'https://www\.notion\.so/[a-f\d]+\?v=[a-f\d]+&pvs=\d+'))
async def get_notion_db_link_and_tasks(message: Message):
    """Добавляем ссылку на notion в бд"""
    db_id = get_notion_db_id(message.text)
    await UserCrud.update_db_link(user_id=message.from_user.id, db_link=db_id)
    await message.answer("Теперь напишите вашу задачу")


@router.message(F.text == "OpenAi update")
async def openai_update(message: Message):
    """Сервисная временная фича"""
    await update_assistant()
    await message.answer("OK")


@router.message(F.text)
async def get_opneai_help(message: Message):
    """Сначала вытаскиваем thread_id из бд, если не находим то создаем новый и добовляем в бд.
    Далее вытаскиваем что имеется в базе данных Notion и форматируем под определнный формат.
    Создаем новое сообщение OpenAI ассистенту с наполнением Notion и с новой тасклй пользователя.
    Получаем ответ от ассистента и закидываем обратно в Notion"""
    if not await UserCrud.get_thread_id(user_id=message.from_user.id):
        thread = await openai_client.beta.threads.create()
        thread_id = thread.id
        await UserCrud.update_thread_id(thread_id=thread_id, user_id=message.from_user.id)
        logging.info('Created thread %s', thread_id)
    else:
        thread_id = await UserCrud.get_thread_id(user_id=message.from_user.id)
        logging.info('Get thread %s', thread_id)

    notion_db_id = await UserCrud.get_database_id(user_id=message.from_user.id)
    notion_db = await notion_client.read_db(database_id=notion_db_id)

    list_of_existing_tasks = []
    for row in notion_db:
        list_of_existing_tasks.append(f"{row['Category']}|{row['Title']}|{row['Priority']}|{row['Due date']}")

    await openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=f"Existing tasks in the notion: {', '.join(map(str, list_of_existing_tasks))}. Here's a new task: {message.text}"
    )
    run = await openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=settings.ASSISTANT_ID
    )

    # tools_to_call = run.required_action.submit_tool_outputs.tool_calls
    # logging.info(tools_to_call)
    #
    # tools_output_array = []
    # for tool in tools_to_call:
    #     tool_call_id = tool.id
    #     function_name = tool.function.name
    #
    #     output = False
    #     if function_name == "insert_task_and_time":
    #         output = True
    #
    #     tools_output_array.append({"tool_call_id": tool_call_id, "output": output})
    #
    # run = await openai_client.beta.threads.runs.submit_tool_outputs(
    #     thread_id=thread_id,
    #     run_id=run.id,
    #     tool_outputs=tools_output_array
    # )

    while run.status not in ["completed", "failed", "requires_action"]:
        run = await openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        await asyncio.sleep(3)
        logging.info("Run status: %s", run.status)

    messages = await openai_client.beta.threads.messages.list(
        thread_id=thread_id
    )
    logging.info("Messages: %s", messages.data[0].content[0].text.value)

    for thread_message in messages.data:
        # Iterate over the 'content' attribute of the ThreadMessage, which is a list
        for content_item in thread_message.content:
            # Assuming content_item is a MessageContentText object with a 'text' attribute
            # and that 'text' has a 'value' attribute, print it
            logging.info(content_item.text.value)

    formatted_task = messages.data[0].content[0].text.value.split('|')
    category = formatted_task[0]
    title = formatted_task[1]
    priority = formatted_task[2]
    due_date = formatted_task[3]
    await notion_client.write_row_in_notion(database_id=notion_db_id,
                                            category=category,
                                            title=title,
                                            priority=priority,
                                            due_date=due_date)

    await message.answer("✅Ваша задача успешно записана✅")


@router.message()
async def any_message(message: Message):
    """Хэндлер который отвечает на любой тип сообщений"""
    await message.answer("...")
