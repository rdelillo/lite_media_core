""" Resolution module.
"""
from typing import Union

import decimal


class ResolutionException(Exception):
    """ Resolution specific exception.
    """


class Resolution(tuple):
    """ Resolution handling.
    """

    def __new__(
        cls,
        width: Union[str, float, int, decimal.Decimal],
        height: Union[str, float, int, decimal.Decimal],
        pixel_aspect_ratio: Union[str, float, int, decimal.Decimal] = 1.0
    ):
        """ Create and return a new Resolution object.

        :raise ResolutionException: when the object could not be created.
        """
        try:
            resolution = tuple.__new__(cls, (int(width), int(height)))
            resolution._pixel_aspect_ratio = float(pixel_aspect_ratio)
            resolution._aspectRatio = None
            return resolution

        except ValueError as error:
            raise ResolutionException(str(error)) from error

    def __str__(self) -> str:
        """ Represent current Resolution object as string.

        :return: The string representation.
        :rtype: str
        """
        return f"{self.width}x{self.height}"

    def __repr__(self):
        """ Represent current Resolution object.

        :return: The object representation.
        :rtype: str
        """
        return "<%s %s pixelAspectRatio=%d>" % (
            self.__class__.__name__,
            self,
            self.pixel_aspect_ratio,
        )

    @property
    def width(self) -> int:
        """ The resolution width.
        """
        return self[0]

    @property
    def height(self) -> int:
        """ The resolution height.
        """
        return self[1]

    @property
    def pixel_aspect_ratio(self) -> float:
        """ The pixel aspect ratio of the resolution.
        """
        return self._pixel_aspect_ratio

    @property
    def aspect_ratio(self) -> float:
        """ The resolution aspect ratio.
        """
        if not self._aspectRatio:  # not often used so delayed computation
            aspectRatio = decimal.Decimal(self.width) / decimal.Decimal(self.height)
            self._aspectRatio = aspectRatio

        return self._aspectRatio

    @classmethod
    def from_string(cls, resolution_str: str):
        """ Create a Resolution object from a resolution string.

        :raise ResolutionException: when the resolution could not be identified.
        """
        try:
            width, height = resolution_str.split("x")
            return cls(width, height)

        except (ValueError, ResolutionException) as error:
            raise ResolutionException(f"Cannot create Resolution object from {resolution_str}.") from error
