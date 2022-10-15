import logging

import httpx

from app.core.exc import SkillBoxNotAuthorized, SkillBoxAPIException
from app.core.types.check_statistics import CheckStatistics

from app.core.types.homework import Homework, HomeworkStatus, HomeworkOrder
from app.core.types.lesson import Lesson
from app.core.types.topic import Topic
from app.core.types.user import User

logger = logging.getLogger(__name__)


class SkillBoxAPI:
    def __init__(self, session: httpx.Client, refresh_token: str):
        self.session = session
        self.refresh_token = refresh_token

    def get_access_token(self) -> str:
        response = self.session.post(
            "https://go.skillbox.ru/api/v1/token/refresh/",
            json={"refresh": self.refresh_token}
        )
        response_data = response.json()
        
        if response_data == 'not valid jwt':
            raise SkillBoxNotAuthorized("Неверный Refresh Token")

        if response_data == "token expired":
            raise SkillBoxNotAuthorized("Закончился срок действия Refresh Token")
        
        if not isinstance(response_data, dict) or "access" not in response_data.keys():
            raise SkillBoxAPIException(f"Непредвиденный ответ сервера: {response.text}")
        
        return response_data["access"]
    
    def check_auth(self) -> bool:
        response = self.session.get("https://go.skillbox.ru/api/v3/websockets/authorize/")
        return response.status_code // 100 == 2

    def auth(self):
        access_token = self.get_access_token()
        self.session.headers.update({
            "x-auth": f"Bearer {access_token}"
        })
    
        if not self.check_auth():
            raise SkillBoxNotAuthorized("Не удалось авторизоваться, попробуйте обновить Refresh Token")
    
    def get_all_homeworks(self, course_uuid: str, status: HomeworkStatus, order: HomeworkOrder) -> list[Homework]:
        url = f"https://go.skillbox.ru/api/v3/teachers/courses/{course_uuid}/homeworks/" \
              f"?ordering={order.value}&status={status.value}"
        homeworks_data = self.session.get(url).json()

        if not isinstance(homeworks_data, dict) or "results" not in homeworks_data.keys():
            raise SkillBoxAPIException(f"Не удалось получить домашние работы")

        result = []
        while True:
            for e in homeworks_data["results"]:
                lesson = Lesson(**e.pop("lesson"))
                topic = Topic(**e.pop("topic"))
                user = User(**e.pop("user"))
                result.append(Homework(**e, lesson=lesson, topic=topic, user=user))
            
            url = homeworks_data["next"]
            if url is None:
                break
            
            homeworks_data = self.session.get(url).json()
            
        return result
    
    def get_check_statistics(self, status: HomeworkStatus) -> list[CheckStatistics]:
        url = f"https://go.skillbox.ru/api/v3/teachers/current/courses/check-statistics/" \
              f"?user_homework_status={status.value}"
        
        check_statistics_data = self.session.get(url).json()
        result = []
        for e in check_statistics_data:
            result.append(CheckStatistics(**e))
            
        return result
