from datetime import datetime, timedelta

from aiogram import Bot

from app.core.client import AsyncSkillBoxAPI
from app.core.types.homework import HomeworkStatus
from bot.config_loader import Config
from bot.core.closer_task import get_closer_task_time


async def notify(api: AsyncSkillBoxAPI, bot: Bot, config: Config):
    text = []

    for course in await api.get_check_statistics(status=HomeworkStatus.WAIT):
        time = await get_closer_task_time(api, course.id)
        delta = time - datetime.now()

        if timedelta(0) < delta < timedelta(hours=1):
            text.append(f"До следующего дедлайна в курсе {course.name} осталось меньше часа")

    if text:
        for admin in config.admins:
            await bot.send_message(admin, "\n\n".join(text))
