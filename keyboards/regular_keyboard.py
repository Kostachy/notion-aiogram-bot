from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

set_openai_buttom: KeyboardButton = KeyboardButton(text='OpenAI-test')


default_keybord: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[set_openai_buttom]],
    resize_keyboard=True
)
