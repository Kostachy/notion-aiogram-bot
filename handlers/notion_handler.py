from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def get_start(message: Message):
    await message.answer('...')



