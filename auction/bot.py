import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from handlers import register_handlers
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import BOT_TOKEN

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт"),
        BotCommand(command="/auction", description="Старт аукциона(только для админов)"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logging.error("Starting bot")

    bot = Bot(token=BOT_TOKEN, parse_mode="html")
    memory = MemoryStorage()
    dp = Dispatcher(bot, storage=memory)

    register_handlers(dp)

    await set_commands(bot)

    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())