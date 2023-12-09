import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.crud.user_crud import UserCrud
from utils import get_notion_db_id

router = Router()


@router.message(CommandStart())
async def get_start(message: Message):
    """Регистрируем юзера"""
    print(await UserCrud.get_user_id(message.from_user.id))
    if not await UserCrud.get_user_id(message.from_user.id):
        await UserCrud.create_user(user_id=message.from_user.id)
    await message.answer('Вы были успешно зарегистрированы!✅\nТеперь введите ссылку на вашу базу данных из Notion')


@router.message(F.text)
async def get_tasks(message: Message):
    db_id = get_notion_db_id(message.text)
    await UserCrud.update_db_link(db_id)
    await message.answer("👍")
