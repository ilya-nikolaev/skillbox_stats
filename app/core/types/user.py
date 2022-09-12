from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    id: str
    last_name: str
    out_key: str
    photo: str
