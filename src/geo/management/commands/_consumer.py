import json
import logging
from json import JSONDecodeError

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from pydantic import ValidationError

from geo.services.city import CityService
from geo.services.schemas import CountryCityDTO

logger = logging.getLogger()


class EventConsumer:
    """
    Функции консьюмера для получения данных из очереди и обработки событий.
    """

    def __init__(self, url: str, queue_name: str):
        """
        Конструктор.

        :param url: Строка подключения к RabbitMQ.
        :param queue_name: Название очереди для получения данных о событиях.
        :return:
        """

        self.queue_name = queue_name

        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True
        )

        channel.start_consuming()
        logger.info("Started events consuming...")

    @staticmethod
    def callback(
        channel: BlockingChannel,  # pylint: disable=unused-argument
        method: Basic.Deliver,  # pylint: disable=unused-argument
        properties: BasicProperties,  # pylint: disable=unused-argument
        body: bytes,
    ) -> None:
        """
        Обработка нового сообщения в очереди.

        :param channel: Канал.
        :param method: Метод доставки сообщения.
        :param properties: Свойства.
        :param body: Данные сообщения.
        :return:
        """

        logger.info("Received event data: %s", body)

        try:
            # преобразование и валидация входящих данных
            data: dict = json.loads(body)
            location = CountryCityDTO(
                city=data.get("city"), alpha2code=data.get("alpha2code")
            )
        except (TypeError, JSONDecodeError, ValidationError):
            logger.error("Error during data parsing.", exc_info=True)

            return

        # импорт данных о городе и стране,
        # если этой информации еще нет в базе данных
        CityService().get_cities(name=location.city)
        logger.info("Location data has been successfully imported.")
