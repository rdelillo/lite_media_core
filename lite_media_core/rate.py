""" Rate module.
"""
from typing import Union, Optional

import abc
import decimal
import math


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


class FrameRateException(ValueError):
    """ Frame Rate specific exception.
    """


class _AbstractFrameRate:
    """ Abstract FrameRate.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, rate: Union[str, float, decimal.Decimal], name: str = None):
        """ Initialize a AbstractFrameRate object.

        :raise FrameRateException: when the input rate is invalid.
        """
        try:
            _ = float(rate)

        except Exception as error:
            raise FrameRateException(f"Cannot build a rate from {rate}.") from error

        if float(rate) < 0 or float(rate) in (math.nan, math.inf):
            raise FrameRateException(f"Cannot build a valid rate from {rate}.")

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

    @staticmethod
    def _conform_to_industry_rate(rate:  Union[str, float, decimal.Decimal]) -> Optional[tuple]:
        """ Compare input rate value against industry standards.
        """
        return next(
            (
                (name, conformed_rate)
                for name, conformed_rate in _INDUSTRY_STANDARD_RATES.items()
                if float(round(conformed_rate, 2)) == float(round(rate, 2))
            ),
            None,
        )

    @staticmethod
    def get_industry_standards() -> dict:
        """ Return defined industry standard rates.
        """
        return _INDUSTRY_STANDARD_RATES.copy()

    @property
    def name(self) -> str:
        """ The rate name.
        """
        return self._name


class FrameRate(_AbstractFrameRate):
    """ Frame handling.
    """

    @property
    def is_standard(self) -> bool:
        """ Is an industry-standard frame rate.
        """
        return self._name in _INDUSTRY_STANDARD_RATES

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
            name, conformed_rate = self._conform_to_industry_rate(float(rate))
            super().__init__(conformed_rate, name=name)

        except ValueError as error:
            raise FrameRateException(f"Cannot initialize frame rate from {rate}.") from error

        except TypeError as error:
            raise FrameRateException(f"Cannot find standard frame rate from {rate}.") from error

    @property
    def is_standard(self) -> bool:
        """ Is an industry-standard frame rate.
        """
        return True
