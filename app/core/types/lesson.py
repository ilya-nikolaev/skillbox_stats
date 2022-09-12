from dataclasses import dataclass
from typing import Optional


@dataclass
class Lesson:
    gitlab_enabled: Optional[bool]
    id: str
    name: str
    number: int
    status: str
    _order: int
