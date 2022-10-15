import sqlite3

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, IDFilter

from app.core.exc import SkillBoxNotAuthorized
from app.core.client import AsyncSkillBoxAPI
from bot.config_loader import Config


async def start_message(m: types.Message):
    await m.answer(
        "<b>Добро пожаловать!</b>\n\n"
        "Обычное сообщение — обновление токена,\n"
        "/overview — информация о количестве работ на проверку,\n"
        "/closer — ближайшие дедлайны по всем курсам.\n\n"
        "Бот доступен только пользователям из белого списка. Приятного использования!"
    )


async def unauthorized_start_message(m: types.Message):
    await m.answer("Бот доступен только пользователям из белого списка, если вышла ошибка — напишите @rnurnu")


async def plain_text(m: types.Message, api: AsyncSkillBoxAPI):
    prev_token = api.refresh_token
    api.refresh_token = m.text

    try:
        await api.auth()
        await m.answer("Refresh Token успешно обновлен!")

        with sqlite3.connect("auth.db") as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE auth_data SET value=? WHERE key='refresh_token'", [m.text])
            connection.commit()

    except SkillBoxNotAuthorized as e:
        await m.answer(f"{e.args[0]}\nУстановлен предыдущий Refresh Token")
        api.refresh_token = prev_token


def register_basic(dp: Dispatcher, config: Config):
    dp.register_message_handler(start_message, Command("start"), IDFilter(config.admins))
    dp.register_message_handler(unauthorized_start_message, Command("start"))
    dp.register_message_handler(plain_text, IDFilter(config.admins))
