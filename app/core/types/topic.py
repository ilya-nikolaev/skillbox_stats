from dataclasses import dataclass


@dataclass
class Topic:
    course_id: str
    id: str
    name: str
    number: int
    _order: int
