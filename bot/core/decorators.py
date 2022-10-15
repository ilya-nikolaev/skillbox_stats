import functools
from typing import Callable

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler

from app.core.exc import SkillBoxNotAuthorized
from app.core.async_client import AsyncSkillBoxAPI


def skillbox_api_required(f: Callable):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        api: AsyncSkillBoxAPI = kwargs["api"]
        try:
            await api.auth()
            return await f(*args, **kwargs)
        except SkillBoxNotAuthorized:
            m: types.Message = args[0]
            await m.answer("Истёк Refresh Token, установите новый")
            raise CancelHandler()

    return wrapper
