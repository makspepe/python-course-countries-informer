from django.db.models import Q, QuerySet

from geo.clients.currency import CurrencyClient
from geo.clients.schemas import CurrencyRatesDTO
from geo.models import Currency, CurrencyRates


class CurrencyService:
    """
    Сервис для работы с данными о валютах.
    """

    def get_currency(self, currency_base: str) -> QuerySet[CurrencyRates]:
        """
        Получение валюты по названию.
        :param str currency_base: название валюты
        :return:
        """
        currency_rates = CurrencyRates.objects.filter(currency__base__icontains=currency_base)
        if not currency_rates:
            currency_data = CurrencyClient().get_rates(currency_base)
            if currency_data:
                currency = Currency.objects.create(base=currency_data.base, date=currency_data.date)
                bulk_rates = [self.build_model_rates(currency, name, rate) for name, rate in currency_data.rates.items()]
                CurrencyRates.objects.bulk_create(bulk_rates, batch_size=1000)
                currency_rates = CurrencyRates.objects.filter(currency__base__icontains=currency.base)
        return currency_rates

    def build_model_rates(
        self, currency: Currency, name: str, rate: float
    ) -> CurrencyRates:
        """
        Формирование объекта модели значения отношений валют.
        :param Currency currency: Валюта
        :param str name: называние валюты
        :param float rate: отношение валют
        :return:
        """
        return CurrencyRates(
            currency=currency,
            currency_name=name,
            rate=rate,
        )

    def build_model(self, currency: CurrencyRatesDTO) -> Currency:
        """
        Формирование объекта модели валюты.
        :param CurrencyRatesDTO currency: Данные о валюте.
        :return:
        """

        return Currency(
            base=currency.base,
            date=currency.date,
        )