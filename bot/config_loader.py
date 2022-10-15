from environs import Env
from dataclasses import dataclass


@dataclass
class Config:
    bot_token: str
    admins: list[int]


def load_config():
    env = Env()
    env.read_env()

    return Config(
        bot_token=env.str("BOT_TOKEN"),
        admins=[int(admin_id) for admin_id in env.list("ADMINS")]
    )
