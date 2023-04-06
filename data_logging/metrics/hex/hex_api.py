import time

import requests

base_url: str = "https://hex.pm/api"


def get_user_owned_packages(username: str) -> list[str]:
    user_info = _send_get_request(f"/users/{username}")
    return list(user_info["owned_packages"].keys())


def get_number_of_all_downloads(package_name: str) -> int:
    package_info = _send_get_request(f"/packages/{package_name}")
    return package_info["downloads"]["all"]


def _send_get_request(endpoint: str, params: dict = {}) -> dict:
    response = requests.get(f"{base_url}{endpoint}", params=params)
    if (
        response.status_code == 429
        and int(response.headers["X-RateLimit-Remaining"]) == 0
    ):
        time_to_sleep = float(response.headers["X-RateLimit-Reset"]) - time.time()
        time.sleep(time_to_sleep)
        return _send_get_request(endpoint, params)
    response.raise_for_status()
    return response.json()
