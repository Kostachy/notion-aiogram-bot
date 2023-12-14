import asyncio
import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
# from states.user_states import UserStates

from config import settings
from db.crud.user_crud import UserCrud
from utils import get_notion_db_id
from notion.notion_api import notion_client

from openai_api.api import openai_client

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
    # await message.answer("""Теперь опишите каждый проект:\nКогда дедлайн(Дата формата YYYY-MM-DD)?\n
    # Какая приоритетность у проекта?(Приоритетность становится выбирается цифрами от 1 до 4 включительно,
    # то есть 1 самая приоритетная, а 4 наименее приоритетная)\nФормат: (категория,задача,приоритетность,дата)""")
    await message.answer("Теперь напишите вашу задачу")


# @router.message(F.text.regexp(r'.*\b([1-4],\d{4}-\d{2}-\d{2})\b.*'))
# async def get_discription_about_tasks(message: Message, state: FSMContext):
#     """Получаем информацию об дедлайнах и приоритетах формат принимаемых данных:
#     (категория,задача,приоритетность,дата)"""
#     data_about_tasks = message.text.split(",")
#     await state.set_state(UserStates.input_data)
#     await state.update_data(category=data_about_tasks[0],
#                             title=data_about_tasks[1],
#                             priority=data_about_tasks[2],
#                             due_date=data_about_tasks[3])
#     # write_dict_to_file_as_json(
#     #     content={"category": category, "title": title, "priority": priority, "due_date": due_date},
#     #     file_name="user_data.json")


@router.message(F.text)
async def get_opneai_help(message: Message):
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
        content=f"Existing tasks in the notion: {', '.join(map(str, list_of_existing_tasks))}\nNew task: {message.text}"
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
        await message.answer(run.status)

    messages = await openai_client.beta.threads.messages.list(
        thread_id=thread_id
    )
    logging.info(messages)
    await message.answer(messages.data[0].content[1].text)
    # await notion_client.simple_write(messages.data[0].content[1].text)


@router.message()
async def any_message(message: Message):
    """Хэндлер который отвечает на любой тип сообщений"""
    await message.answer("...")
