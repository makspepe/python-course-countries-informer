"""
Функции для взаимодействия с внешним сервисом-провайдером данных о курсах валют.
"""
from typing import Optional

from app.settings import API_KEY_APILAYER
from base.clients.base import BaseClient
from geo.clients.schemas import CurrencyRatesDTO


class CurrencyClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о курсах валют.
    """

    headers = {"apikey": API_KEY_APILAYER}

    def get_base_url(self) -> str:
        return "https://api.apilayer.com/fixer/latest"

    def get_rates(self, base: str = "rub") -> Optional[CurrencyRatesDTO]:
        """
        Получение данных о курсах валют.
        :param base: Базовая валюта
        :return:
        """
        self.params["base"] = base
        data = self._request(self.get_base_url())
        if not data:
            return None
        return CurrencyRatesDTO(
            base=data["base"], date=data["date"], rates=data["rates"]
        )
