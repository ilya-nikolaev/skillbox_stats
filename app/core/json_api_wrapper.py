import json
import logging

import requests

logger = logging.getLogger(__name__)


class JSONAPIWrapper:
    def __init__(self, session: requests.Session):
        self.session = session
    
    def send_post_request(self, url: str, json_data: dict):
        try:
            response = self.session.post(url, json=json_data)
        except requests.exceptions.RequestException as e:
            logger.error("Ошибка соединения")
            raise e
        
        return response
    
    def send_get_request(self, url: str):
        try:
            response = self.session.get(url)
        except requests.exceptions.RequestException as e:
            logger.error("Ошибка соединения")
            raise e
        
        return response
    
    @staticmethod
    def parse_json(response: requests.Response):
        try:
            response_data = response.json()
        except json.decoder.JSONDecodeError as e:
            logger.error(f"Невалидный JSON: {response.text}")
            raise e
        
        return response_data
