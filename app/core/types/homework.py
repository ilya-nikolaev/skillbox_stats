from enum import Enum
from dataclasses import dataclass
from typing import Optional

from app.core.types.lesson import Lesson
from app.core.types.topic import Topic
from app.core.types.user import User


@dataclass
class Homework:
    check_status: str
    id: str
    iteration: int
    last_active_at: str
    lesson: Lesson
    lesson_id: str
    status: str
    status_updated_at: str
    teacher_feedback: Optional[str]
    topic: Topic
    topic_id: str
    user: User
    user_id: str


class HomeworkStatus(Enum):
    DONE = "done"
    WAIT = "wait"
    FAIL = "fail"


class HomeworkOrder(Enum):
    OLD = "last_active_at"
    NEW = "-last_active_at"
