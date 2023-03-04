"""
Базовые функции для клиентов внешних сервисов.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from http import HTTPStatus
import httpx
from app.settings import REQUESTS_TIMEOUT


class BaseClient(ABC):
    """
    Базовый класс, реализующий интерфейс для клиентов.
    """

    headers: dict[str, Any] = {}
    params: dict[str, Any] = {}

    @abstractmethod
    def get_base_url(self) -> str:
        """
        Получение базового URL для запросов.
        :return:
        """

    def _request(self, endpoint: str) -> Optional[dict]:
        """
        Формирование и выполнение запроса.
        :param endpoint:
        :return:
        """
        try:
            with httpx.Client(timeout=REQUESTS_TIMEOUT) as client:
                response = client.get(
                    endpoint, headers=self.headers, params=self.params
                )
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, httpx.TimeoutException, httpx.RequestError) as e:
            print(f"An error occurred: {e}")
            return {}
