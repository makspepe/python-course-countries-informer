"""
Описание моделей данных (DTO).
"""

from pydantic import Field

from base.clients.schemas import HashableBaseModel


class CountryCityDTO(HashableBaseModel):
    """
    Модель данных для идентификации города.
    Содержит ISO Alpha2-код страны и название города.

    .. code-block::

        CountryCityDTO(
            city="Mariehamn",
            alpha2code="AX",
        )
    """

    city: str
    alpha2code: str = Field(min_length=2, max_length=2)
