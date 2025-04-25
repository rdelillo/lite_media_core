""" Rate module.
"""
from typing import Union, Optional

import abc
import decimal


# The following standards are the most common ones from the industry:
_INDUSTRY_STANDARD_RATES = {
    "Film with NTSC compatibility": decimal.Decimal(24) * (decimal.Decimal(1000) / decimal.Decimal(1001)),
    "Film": decimal.Decimal(24),
    "PAL/SECAM video": decimal.Decimal(25),
    "PAL/SECAM video with NTSC compatibility": decimal.Decimal(25) * (decimal.Decimal(1000) / decimal.Decimal(1001)),
    "NTSC video": decimal.Decimal(30) * (decimal.Decimal(1000) / decimal.Decimal(1001)),
    "Black and white NTSC": decimal.Decimal(30),
    "Trial Hight FPS": decimal.Decimal(48),
    "HD-TV": decimal.Decimal(50),
    "High definition video - NTSC": decimal.Decimal(60) * (decimal.Decimal(1000) / decimal.Decimal(1001)),
    "UHD-TV": decimal.Decimal(100),
}


class FrameRateException(Exception):
    """ Frame Rate specific exception.
    """


class _AbstractFrameRate:
    """ Abstract FrameRate.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, rate: Union[str, float, decimal.Decimal], name: str = None):
        """ Initialize a AbstractFrameRate object.
        """
        self._rate = rate
        self._name = name

    def __str__(self) -> str:
        """ Represent current AbstractFrameRate object as string.
        """
        return f"{float(self)} fps"

    def __float__(self) -> float:
        """ Convert to float.
        """
        return round(float(self._rate), 2)

    def __repr__(self) -> str:
        """ Represent the AbstractFrameRate.
        """
        return f"<{self.__class__.__name__} {self} {self._name}>"

    def __eq__(self, other: object) -> bool:
        """ Is equal ?
        """
        try:
            return float(self) == float(other)

        except (ValueError, TypeError):
            raise ValueError("Invalid comparison between FrameRate and {other}.")

    def __ne__(self, other: object) -> bool:
        """ Override the default "not equals" behavior.
        """
        return not self == other

    @property
    def name(self) -> str:
        """ The rate name.
        """
        return self._name


class FrameRate(_AbstractFrameRate):
    """ Frame handling.
    """

    @classmethod
    def from_custom_value(cls, rate: Union[str, float, int, decimal.Decimal]):
        """ Create a frame rate object from any value.
        """
        try:
            return StandardFrameRate(rate)

        except FrameRateException:  # non-standard
            return FrameRate(rate, name="custom rate")


class StandardFrameRate(_AbstractFrameRate):
    """ Industry standard frame rates handling.
    """

    def __init__(self, rate: Union[str, float, decimal.Decimal], name: str = None):
        """ Initialize a FrameRate object.

        :raise FrameRateException: when the input rate is either invalid or not standard.
        """
        try:
            name, conformed_rate = _conform_to_industry_rate(float(rate))
            super().__init__(conformed_rate, name=name)

        except ValueError as error:
            raise FrameRateException(f"Cannot initialize frame rate from {rate}.") from error

        except TypeError as error:
            raise FrameRateException(f"Cannot find standard frame rate from {rate}.") from error


def _conform_to_industry_rate(rate:  Union[str, float, decimal.Decimal]) -> Optional[tuple]:
    """ Compare input rate value against industry standards.
    """
    for name, conformed_rate in _INDUSTRY_STANDARD_RATES.items():
        if float(round(conformed_rate, 2)) == float(round(rate, 2)):
            return name, conformed_rate

    return None
