import requests

from app.core.skillbox_api import SkillBoxApi
from app.core.helper import get_refresh_token
from app.core.types.homework import HomeworkOrder, HomeworkStatus


def main():
    session = requests.Session()
    skillbox_api = SkillBoxApi(session, get_refresh_token("refresh_token.txt"))
    skillbox_api.auth()
    
    print(
        *skillbox_api.get_check_statistics(
            HomeworkStatus.DONE
        ), sep="\n"
    )
    

if __name__ == "__main__":
    main()
