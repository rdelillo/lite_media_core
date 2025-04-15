""" Resolution module.

:Example:

>>> from lite_media_core import resolution
>>> res = resolution.Resolution(1920, 1080)
>>> str(res)
'1920x1080'
>>> res.width
1920
>>> res.height
1080
>>> w, h = res ; assert (w, h) == (1920, 1080)
True
>>> res.aspectRatio
decimal.Decimal(1.777777777778)
>>> res.pixelAspectRatio
1.0
>>> resolution.Resolution.fromString("1920x1080")
resolution.Resolution(1920, 1080)
"""
import decimal


class ResolutionException(Exception):
    """ Resolution specific exception.
    """


class Resolution(tuple):
    """ Resolution handling.
    """
    def __new__(cls, width, height, pixelAspectRatio=1.0):
        """ Create and return a new Resolution object.

        :param width: The resolution width.
        :type width: str or float or int or double
        :param height: The resolution height.
        :type height: str or float or int or double
        :param pixelAspectRatio: An optional pixel aspect ratio.
        :type pixelAspectRatio: str or float or int or double.
        :return: the created Resolution object.
        :rtype: :class:`Resolution`
        :raise ResolutionException: when the object could not be created.
        """
        try:
            resolution = tuple.__new__(cls, (int(width), int(height)))
            resolution._pixelAspectRatio = float(pixelAspectRatio)
            resolution._aspectRatio = None
            return resolution

        except ValueError as error:
            raise ResolutionException(str(error)) from error

    def __str__(self):
        """ Represent current Resolution object as string.

        :return: The string representation.
        :rtype: str
        """
        return "%sx%s" % (self.width, self.height)

    def __repr__(self):
        """ Represent current Resolution object.

        :return: The object representation.
        :rtype: str
        """
        return "<%s %s pixelAspectRatio=%d>" % (
            self.__class__.__name__,
            self,
            self.pixelAspectRatio,
        )

    @property
    def width(self):
        """
        :return: The resolution width.
        :rtype: int
        """
        return self[0]

    @property
    def height(self):
        """
        :return: The resolution height.
        :rtype: int
        """
        return self[1]

    @property
    def pixelAspectRatio(self):
        """
        :return: The pixel aspect ratio.
        :rtype: float
        """
        return self._pixelAspectRatio

    @property
    def aspectRatio(self):
        """
        :return: The resolution aspect ratio.
        :rtype: :class:`decimal.Decimal`
        """
        if not self._aspectRatio:  # not often used so delayed computation
            aspectRatio = decimal.Decimal(self.width) / decimal.Decimal(self.height)
            self._aspectRatio = aspectRatio

        return self._aspectRatio

    @classmethod
    def fromString(cls, resolutionStr):
        """ Create a Resolution object from a resolution string.

        :param str resolutionStr: The resolution string.
        :return: The Resolution object.
        :rtype: :class:`Resolution`
        :raise ResolutionException: when the resolution could not be identified.
        """
        try:
            width, height = resolutionStr.split("x")
            return cls(width, height)

        except (ValueError, ResolutionException) as error:
            raise ResolutionException("Cannot create Resolution object from %r." % resolutionStr) from error
