from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from app.core.client import AsyncSkillBoxAPI


class SkillBoxAPIMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, skillbox_api: AsyncSkillBoxAPI):
        self.api = skillbox_api
        super().__init__()

    async def pre_process(self, obj, data, *args):
        data["api"] = self.api
