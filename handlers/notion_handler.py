import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.crud.user_crud import UserCrud
from utils import get_notion_db_id
from notion.notion_api import client
from openai_api.api import openai_client

router = Router()


@router.message(CommandStart())
async def get_start(message: Message):
    """Регистрируем юзера"""
    if not await UserCrud.get_user_id(message.from_user.id):
        await UserCrud.create_user(user_id=message.from_user.id)
        thread = openai_client.create_thread()
        await UserCrud.update_thread_id(thread_id=thread.id, user_id=message.from_user.id)
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
    thread = await UserCrud.get_thread_id(user_id=message.from_user.id)
    print(thread)
    await openai_client.add_message_to_thread(thread=thread.id, message_id=message.text)
    await message.answer("")


@router.message()
async def any_message(message: Message):
    """Хэндлер который отвечает на любой тип сообщений"""
    await message.answer("...")
