import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.crud.user_crud import UserCrud

router = Router()


@router.message(CommandStart())
async def get_start(message: Message):
    """Регистрируем юзера"""
    result = await UserCrud().get_user_id(1)
    print(result[0])
    await message.answer('Введите категории ваших задач через пробел')



@router.message(F.text)
async def get_tasks(message: Message):
    global data
    data['tasks'] = ['Task_Name']
    logging.info(data)
    await message.answer("👍")




