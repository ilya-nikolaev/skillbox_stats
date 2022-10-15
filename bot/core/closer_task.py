from datetime import datetime, timedelta, tzinfo
from typing import Optional

from app.core.client import AsyncSkillBoxAPI
from app.core.types.homework import HomeworkStatus, HomeworkOrder, Homework


def get_deadline(homework: Homework):
    start_time = datetime.fromisoformat(homework.status_updated_at)

    if start_time.weekday() in (3, 5, 6):
        delta = timedelta(days=2)
    elif start_time.weekday() == 4:
        delta = timedelta(days=3)
    else:
        delta = timedelta(days=1)

    return start_time + delta


async def get_closer_task_time(api: AsyncSkillBoxAPI, course_id: str) -> Optional[datetime]:
    homeworks = await api.get_all_homeworks(course_id, status=HomeworkStatus.WAIT, order=HomeworkOrder.NEW)
    try:
        return min(
            deadline for homework in homeworks if
            (deadline := get_deadline(homework)) > datetime.now(deadline.tzinfo)
        )
    except ValueError:
        return None
