import asyncio
import logging
import sqlite3

import requests
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from app.core.skillbox_api import SkillBoxAPI
from bot.config_loader import load_config, Config
from bot.handlers.basic import register_basic
from bot.handlers.overview import register_overview
from bot.middlewares.skillbox_middleware import SkillBoxAPIMiddleware


def setup_handlers(dp: Dispatcher, config: Config):
    register_overview(dp, config)
    register_basic(dp, config)


def setup_middlewares(dp: Dispatcher, api: SkillBoxAPI):
    dp.middleware.setup(SkillBoxAPIMiddleware(api))


def init_db_parameters() -> str:
    with sqlite3.connect("auth.db") as connection:
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS auth_data (key TEXT PRIMARY KEY, value TEXT)")
        connection.commit()

        cursor.execute("SELECT value FROM auth_data WHERE key='refresh_token'")
        refresh_token = cursor.fetchone()
        if refresh_token is not None:
            return refresh_token[0]


async def main():
    logging.basicConfig(
        format=u"%(filename)s:%(lineno)-d #%(levelname)-16s [%(asctime)s] %(message)s",
        level=logging.INFO
    )

    config: Config = load_config()

    bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)

    setup_handlers(dp, config)

    refresh_token = init_db_parameters()
    if refresh_token is None:
        logging.error("Не установлен Refresh Token")
        return

    sync_session = requests.Session()
    skillbox_api = SkillBoxAPI(
        session=sync_session,
        refresh_token=refresh_token
    )

    setup_middlewares(dp, skillbox_api)

    try:
        logging.info("Bot is starting...")
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
