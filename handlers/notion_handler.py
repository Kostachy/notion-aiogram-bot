import asyncio
import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

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
    await message.answer("Теперь передайте мне вашу задачу и время")


@router.message(F.text)
async def get_opneai_help(message: Message):
    if not await UserCrud.get_thread_id(user_id=message.from_user.id):
        thread = await openai_client.beta.threads.create()
        thread_id = thread.id
    else:
        thread_id = await UserCrud.get_thread_id(user_id=message.from_user.id)

    await openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message.text
    )
    run = await openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=settings.ASSISTANT_ID
    )
    while run.status not in ["completed", "failed", "requires_action"]:
        run = await openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        await asyncio.sleep(3)
        await message.reply(run.status)
    tools_to_call = run.required_action.submit_tool_outputs.tool_calls
    tools_output_array = []
    for tool in tools_to_call:
        tool_call_id = tool.id
        function_name = tool.function.name

        output = False
        if function_name == "insert_task_and_time":
            output = True

        tools_output_array.append({"tool_call_id": tool_call_id, "output": output})

    run = await openai_client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run.id,
        tool_outputs=tools_output_array
    )

    while run.status not in ["completed", "failed", "requires_action"]:
        run = await openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        await message.reply(run.status)

    messages = openai_client.beta.threads.messages.list(
        thread_id=thread_id
    )

    for text in messages:
        await message.answer(text.content[0].text.value)


@router.message()
async def any_message(message: Message):
    """Хэндлер который отвечает на любой тип сообщений"""
    await message.answer("...")
