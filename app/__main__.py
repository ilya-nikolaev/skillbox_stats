import httpx

from app.core.exc import SkillBoxNotAuthorized
from app.core.sync_client.skillbox_api import SkillBoxAPI
from app.helper import get_refresh_token
from app.core.types.homework import HomeworkStatus


def main():
    session = httpx.Client()
    skillbox_api = SkillBoxAPI(session, get_refresh_token())
    while True:
        try:
            skillbox_api.auth()
            break
        except SkillBoxNotAuthorized:
            skillbox_api.refresh_token = get_refresh_token(wrong_token=True)
    
    print(*skillbox_api.get_check_statistics(
        HomeworkStatus.DONE
    ), sep="\n")


if __name__ == "__main__":
    main()
