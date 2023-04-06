"""
Модуль содержит функции для работы с API
"""
import json
import logging

import requests
from requests import ReadTimeout, adapters

from spawn import env

API_BASE_URL = env.str("API_BASE_URL", "http://127.0.0.1:8000")


def create_bookmark(telegram_id: str, url: str) -> dict | None:
    """
    Post URL and user's `telegram_id` to API to create new bookmark for this user.

    Reference: https://requests.readthedocs.io/en/latest/user/quickstart/#more-complicated-post-requests
    """
    api_url = API_BASE_URL + "/api/v1/bookmarks/create_from_telegram/"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "user": {
            "telegram_id": telegram_id,
        },
        "url": url,
    }

    try:
        # Делаем запрос c тайм-аутом 10 с, три попытки (в случае истечения тайм-аута)
        session = requests.Session()
        adapter = adapters.HTTPAdapter(max_retries=3)
        session.mount("http://", adapter)
        response = session.post(
            url=api_url,
            headers=headers,
            data=json.dumps(data),
            timeout=10,
        )
    except ReadTimeout:
        logging.error("Connection timed out (after 3 retries).")
        return None
    except Exception as e:
        logging.error("Connection error.", e)
        return None

    if response:
        # 201 == created:
        if response.status_code == 201:
            result = json.loads(response.text)
            return result

    return None
