"""
Функции для взаимодействия с внешним сервисом-провайдером новостной ленты.
"""
from http import HTTPStatus
from typing import Optional

import httpx

from app.settings import REQUESTS_TIMEOUT, API_KEY_NEWSAPI
from base.clients.base import BaseClient

from news.clients.schemas import NewsItemDTO


class NewsClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером новостной ленты.
    """

    def get_base_url(self) -> str:
        return "https://newsapi.org/v2"

    def get_news(self, alpha2code: str) -> Optional[list[NewsItemDTO]]:
        """
        Получение новостной ленты для указанной страны.

        :param alpha2code: ISO Alpha2 код страны
        :return:
        """

        if response := self._request(
            f"{self.get_base_url()}/top-headlines?country={alpha2code}&category=general&apiKey={API_KEY_NEWSAPI}"
        ):
            items = []
            for item in response["articles"]:
                items.append(
                    NewsItemDTO(
                        source=item["source"]["name"],
                        author=item["author"],
                        title=item["title"],
                        description=item["description"],
                        url=item["url"],
                        published_at=item["publishedAt"],
                    )
                )

            return items

        return None
