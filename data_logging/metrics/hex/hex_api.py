import requests
import time

class HexAPI:
    base_url: str = "https://hex.pm/api"

    @staticmethod
    def get_user_owned_packages(username: str) -> list[str]:
        user_info = _send_get_request(f"/users/{username}")
        return list(user_info["owned_packages"].keys())

    @staticmethod
    def get_number_of_all_downloads(package_name) -> int:
        package_info = _send_get_request(f"/packages/{package_name}")
        return package_info["downloads"]["all"]
    

def _send_get_request(
    endpoint: str, params: dict = {}
) -> dict:
    response = requests.get(f"{HexAPI.base_url}{endpoint}", params=params)
    response.raise_for_status()
    if response.headers["X-RateLimit-Remaining"] == 0:
        time_to_sleep = float(response.headers["X-RateLimit-Reset"]) - time.time() 
        time.sleep(time_to_sleep)
    return response.json()