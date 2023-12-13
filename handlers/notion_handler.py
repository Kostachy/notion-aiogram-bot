import logging
from pprint import pprint

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.crud.user_crud import UserCrud
from keyboards.regular_keyboard import default_keybord
from utils import get_notion_db_id
from notion.notion_api import client
from openai_api.api import openai_client

router = Router()


@router.message(CommandStart())
async def get_start(message: Message):
    """Регистрируем юзера"""
    if not await UserCrud.get_user_id(message.from_user.id):
        await UserCrud.create_user(user_id=message.from_user.id)
    await message.answer('Вы были успешно зарегистрированы!✅\nТеперь введите ссылку на вашу базу данных из Notion',
                         reply_markup=default_keybord)


@router.message(F.text.regexp(r'https://www\.notion\.so/[a-f\d]+\?v=[a-f\d]+&pvs=\d+'))
async def get_notion_db_link_and_tasks(message: Message):
    """Добавляем ссылку на notion в бд"""
    db_id = get_notion_db_id(message.text)
    await UserCrud.update_db_link(user_id=message.from_user.id, db_link=db_id)
    db_rows = await client.read_db(database_id=db_id)
    await message.answer(f"{db_rows}", reply_markup=default_keybord)


@router.message(F.text)
async def get_ai_help(message: Message):
    assistant_object = await openai_client.create_assistant()
    thread = await openai_client.create_thread()
    await openai_client.add_message_to_thread(thread, message.text)
    await openai_client.run_assistant(thread, assistant_object)
    message_from_ai = await openai_client.display_assistant_responce(thread)
    pprint(message_from_ai)
    await message.answer("OK")
