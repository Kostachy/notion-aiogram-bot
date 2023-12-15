import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from handlers.notion_handler import router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    storage = MemoryStorage()
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
