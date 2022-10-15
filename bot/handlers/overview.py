from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import IDFilter, Command

from app.core.skillbox_api import SkillBoxAPI
from app.core.types.homework import HomeworkStatus
from bot.config_loader import Config
from bot.core.closer_task import get_closer_task_time
from bot.core.decorators import skillbox_api_required


@skillbox_api_required
async def show_current_tasks(m: types.Message, api: SkillBoxAPI):
    stats = api.get_check_statistics(status=HomeworkStatus.WAIT)

    await m.answer("\n\n".join(
        f"<b>{e.name}</b>\n"
        f"Работ ожидающих проверки: {e.homeworks_count}\n"
        f"Работ в красной зоне: {e.homeworks_count_danger}"
        for e in stats
    ))


@skillbox_api_required
async def show_closer_tasks(m: types.Message, api: SkillBoxAPI):
    course_uuids = [(e.id, e.name) for e in api.get_check_statistics(status=HomeworkStatus.WAIT)]

    res = []
    for course_id, name in course_uuids:
        deadline = get_closer_task_time(api, course_id)
        res.append((name, deadline))

    await m.answer("\n\n".join(
        f"<b>{name}</b>\n"
        f"Ближайший дедлайн: {deadline.strftime('%d.%m %H:%M') if deadline is not None else 'не скоро'}"
        for name, deadline in res
    ))


def register_overview(dp: Dispatcher, config: Config):
    dp.register_message_handler(show_current_tasks, IDFilter(config.admins), Command("overview"))
    dp.register_message_handler(show_closer_tasks, IDFilter(config.admins), Command("closer"))
