""" Rate module.

:Example:

>>> from lite_media_core import rate
>>> frameRate = rate.FrameRate("24")
>>> str(frameRate)
'24.0 fps'
>>> repr(frameRate)
'<FrameRate 24.0 fps Film>'
>>> customFrameRate = rate.FrameRate.fromCustomRate(11.1)
>>> repr(customRate)
'<CustomFrameRate 11.1 fps custom rate>'
"""
import abc
import decimal


# Technically any speed could be used as a video frame rate. This is true with the latest media players.
# However before the industry went digital, it was shot on film and so it kept some standards from analogical
# times. The following standards are the most common ones from the industry:
# http://documentation.apple.com/en/finalcutpro/usermanual/index.html#chapter=D%26section=4%26tasks=true
# https://en.wikipedia.org/wiki/List_of_broadcast_video_formats
_STANDARD_RATES = {
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

    def __init__(self, rate, name=None):
        """ Initialize a AbstractFrameRate object.

        :param rate: The frame rate value.
        :type rate: str or float or int or decimal.Decimal
        :param str name: The frame rate name.
        """
        self._rate = rate
        self._name = name

    def __str__(self):
        """ Represent current AbstractFrameRate object as string.

        :return: The string representation.
        :rtype: str
        """
        return "%s fps" % float(self)

    def __float__(self):
        """ Represent current AbstractFrameRate object as float.

        :return: The float representation.
        :rtype: float
        """
        return round(float(self._rate), 2)

    def __repr__(self):
        """ Represent current AbstractFrameRate object.

        :return: The object representation.
        :rtype: str
        """
        return "<%s %s %s>" % (self.__class__.__name__, self, self._name)

    def __eq__(self, other):
        """ Override the default "equals" behavior.

        :param object other: An object to compare against.
        :return: is equal to other object.
        :rtype: bool
        """
        try:
            return float(self) == float(other)

        except (ValueError, TypeError) as error:
            raise type(error)("Invalid comparison between FrameRate and %r." % other)

    def __ne__(self, other):
        """ Override the default "not equals" behavior.

        :param object other: An object to compare against.
        :return: is not equal to other object.
        :rtype: bool
        """
        return not self == other

    @property
    def name(self):
        """
        :return: The rate name.
        :rtype: str
        """
        return self._name


class FrameRate(_AbstractFrameRate):
    """ Industry standard frame rates handling.
    """

    def __init__(self, rate):
        """ Initialize a AbstractFrameRate object.

        :param rate: The rate value.
        :type rate: str or float or int or decimal.Decimal
        :raise FrameRateException: when the input rate is invalid or not standard.
        """
        try:
            name, conformedRate = _conformToIndustryRate(float(rate))
            super().__init__(conformedRate, name=name)

        except TypeError as error:
            raise FrameRateException("Cannot find standard frame rate from %r." % rate) from error

        except ValueError as error:
            raise FrameRateException("Cannot initialise frame rate from %r." % rate) from error

    @classmethod
    def fromCustomRate(cls, rate):
        """ Create a frame rate object from a custom rate value.

        :param rate: The rate value.
        :type rate: str or float or int or decimal.Decimal
        :return: The frame rate object.
        :rtype: :class:`FrameRate` or :class:`CustomFrameRate`
        """
        try:
            return cls(rate)

        except FrameRateException:
            return CustomFrameRate(rate, name="custom rate")


class CustomFrameRate(_AbstractFrameRate):
    """ Custom frame rates handling.
    """


def _conformToIndustryRate(rate):
    """ Conform input rate value against industry standards.

    :param float rate: The frame rate to inspect.
    :return: The standard name and conformed rate.
    :rtype: tuple or None
    """
    for name, conformedRate in _STANDARD_RATES.items():
        if float(round(conformedRate, 2)) == float(round(rate, 2)):
            return name, conformedRate

    return None
