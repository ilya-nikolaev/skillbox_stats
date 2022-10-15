import functools
import logging
from typing import Callable

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler

from app.core.exc import SkillBoxNotAuthorized
from app.core.skillbox_api import SkillBoxAPI


def skillbox_api_required(f: Callable):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        api: SkillBoxAPI = kwargs["api"]
        try:
            api.auth()
            return await f(*args, **kwargs)
        except SkillBoxNotAuthorized:
            m: types.Message = args[0]
            await m.answer("Истёк Refresh Token, установите новый")
            raise CancelHandler()

    return wrapper
