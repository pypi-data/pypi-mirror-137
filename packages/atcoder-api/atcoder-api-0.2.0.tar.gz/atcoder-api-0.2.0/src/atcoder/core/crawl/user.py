import requests

from atcoder.core.crawl.constant import USERS_URL


async def get_user_profile_page(
    user_id: str,
) -> requests.models.Response:
    url = f"{USERS_URL}/{user_id}"
    return requests.get(url)


async def get_user_competition_history_page(
    user_id: str,
) -> requests.models.Response:
    url = f"{USERS_URL}/{user_id}/history"
    return requests.get(url)
