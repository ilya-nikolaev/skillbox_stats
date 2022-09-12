from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckStatistics:
    display_order: Optional[int]
    homeworks_count: int
    homeworks_count_danger: int
    id: str
    image: Optional[str]
    is_diploma: bool
    name: str
    slug: str
