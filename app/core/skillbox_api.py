import logging

import requests

from app.core.json_api_wrapper import JSONAPIWrapper
from app.core.types.check_statistics import CheckStatistics

from app.core.types.homework import Homework, HomeworkStatus, HomeworkOrder
from app.core.types.lesson import Lesson
from app.core.types.topic import Topic
from app.core.types.user import User

logger = logging.getLogger(__name__)


class SkillBoxApi(JSONAPIWrapper):
    def __init__(self, session: requests.Session, refresh_token: str):
        self.refresh_token = refresh_token
        super(SkillBoxApi, self).__init__(session)

    def get_access_token(self) -> str:
        response = self.send_post_request(
            "https://go.skillbox.ru/api/v1/token/refresh/",
            json_data={"refresh": self.refresh_token}
        )
        response_data = self.parse_json(response)
        
        if response_data == 'not valid jwt':
            raise ValueError("Неверный Refresh Token")
        
        if not isinstance(response_data, dict) or "access" not in response_data.keys():
            raise ValueError(f"Непредвиденный ответ сервера: {response.text}")
        
        return response_data["access"]
    
    def check_auth(self) -> bool:
        response = self.send_get_request("https://go.skillbox.ru/api/v3/websockets/authorize/")
        return response.ok

    def auth(self):
        access_token = self.get_access_token()
        self.session.headers.update({
            "x-auth": f"Bearer {access_token}"
        })
    
        if not self.check_auth():
            raise ValueError("Не удалось авторизоваться, попробуйте обновить Refresh Token")
    
    def get_all_homeworks(self, course_uuid: str, status: HomeworkStatus, order: HomeworkOrder) -> list[Homework]:
        url = f"https://go.skillbox.ru/api/v3/teachers/courses/{course_uuid}/homeworks/" \
              f"?ordering={order.value}&status={status.value}"
        homeworks_data = self.parse_json(self.send_get_request(url))

        if not isinstance(homeworks_data, dict) or "results" not in homeworks_data.keys():
            raise ValueError(f"Не удалось получить домашние работы")

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
            
            homeworks_data = self.parse_json(self.send_get_request(url))
            
        return result
    
    def get_check_statistics(self, status: HomeworkStatus) -> list[CheckStatistics]:
        url = f"https://go.skillbox.ru/api/v3/teachers/current/courses/check-statistics/" \
              f"?user_homework_status={status.value}"
        
        check_statistics_data = self.parse_json(self.send_get_request(url))
        result = []
        for e in check_statistics_data:
            result.append(CheckStatistics(**e))
            
        return result
