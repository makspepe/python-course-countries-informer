"""
Функции для взаимодействия с внешним сервисом-провайдером данных о странах.
"""
from http import HTTPStatus
from typing import Optional

import httpx

from app.settings import API_KEY_APILAYER, REQUESTS_TIMEOUT
from base.clients.base import BaseClient
from geo.clients.schemas import CountryDTO, CurrencyInfoDTO, CityDTO, CountryShortDTO


class GeoClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о странах и городах.
    """

    def get_base_url(self) -> str:
        return "https://api.apilayer.com/geo"

    def _request(self, endpoint: str) -> Optional[dict]:
        with httpx.Client(timeout=REQUESTS_TIMEOUT) as client:
            # формирование заголовков запроса
            headers = {"apikey": API_KEY_APILAYER}
            # получение ответа
            response = client.get(endpoint, headers=headers)
            if response.status_code == HTTPStatus.OK:
                return response.json()

            return None

    def get_countries(self, name: str) -> Optional[list[CountryDTO]]:
        """
        Получение данных о странах по названию.

        :param name: Название страны
        :return:
        """

        if response := self._request(f"{self.get_base_url()}/country/name/{name}"):
            items = []
            for item in response:
                items.append(
                    CountryDTO(
                        name=item["name"],
                        alpha2code=item["alpha2code"],
                        alpha3code=item["alpha3code"],
                        capital=item["capital"],
                        region=item["region"],
                        subregion=item["subregion"],
                        population=item["population"],
                        latitude=item["latitude"],
                        longitude=item["longitude"],
                        demonym=item["demonym"],
                        area=item["area"],
                        numeric_code=item["numeric_code"],
                        flag=item["flag"],
                        currencies={
                            CurrencyInfoDTO(code=currency["code"])
                            for currency in item["currencies"]
                        },
                        languages=item["languages"],
                    )
                )

            return items

        return None

    def get_country_by_code(self, code: str) -> Optional[CountryDTO]:
        """
        Получение данных о странах по коду (ISO Alpha3).

        :param code: ISO Alpha3 код
        :return:
        """

        if response := self._request(f"{self.get_base_url()}/country/code/{code}"):
            item = response[0]
            return CountryDTO(
                name=item["name"],
                alpha2code=item["alpha2code"],
                alpha3code=item["alpha3code"],
                capital=item["capital"],
                region=item["region"],
                subregion=item["subregion"],
                population=item["population"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                demonym=item["demonym"],
                area=item["area"],
                numeric_code=item["numeric_code"],
                flag=item["flag"],
                currencies={
                    CurrencyInfoDTO(code=currency["code"])
                    for currency in item["currencies"]
                },
                languages=item["languages"],
            )

        return None

    def get_cities(self, name: str) -> Optional[list[CityDTO]]:
        """
        Получение данных о городах по названию.

        :param name: Название города
        :return:
        """

        if response := self._request(f"{self.get_base_url()}/city/name/{name}"):
            items = []
            for item in response:
                items.append(
                    CityDTO(
                        name=item["name"],
                        state_or_region=item["state_or_region"],
                        country=CountryShortDTO(
                            name=item["country"]["name"],
                            alpha2code=item["country"]["code"],
                        ),
                        latitude=item["latitude"],
                        longitude=item["longitude"],
                    )
                )

            return items

        return None
