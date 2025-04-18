""" Single file object.
"""
import os

from lite_media_core.path_utils import sequence


class SingleFile:
    """ A SingleFile object represent an individual unpadded file which is not a Sequence.
    """

    def __init__(self, path):
        """ Initialize the SingleFile.

        :param str path: The single file path.
        """
        self._path = path

    def __eq__(self, other):
        """
        :param other: Another object
        :type other: :class:`SingleFile` or :class:`Sequence`
        :return: True if both sequences are equal. False otherwise.
        :rtype: bool
        """
        if isinstance(other, sequence.Sequence):
            return os.path.abspath(self._path) == other.start == other.end

        return repr(self) == repr(other)

    def __ne__(self, other):
        """
        :param other: Another SingleFile object
        :type other: :class:`SingleFile` or :class:`Sequence`
        :return: True if both sequences and different. False otherwise.
        :rtype: bool
        """
        return repr(self) != repr(other)

    def __hash__(self):
        """
        :return: A hashed representation of the SingleFile.
        :rtype: int
        """
        return hash(repr(self))

    def __repr__(self):
        """
        :return: The representation of the SingleFile.
        :rtype: str
        """
        return "<%s %r>" % (self.__class__.__name__, self._path)

    def __str__(self):
        """
        :return: The string representation of the SingleFile.
        :rtype: str
        """
        return self._path

    def __iter__(self):
        """
        :return: The path of the SingleFile.
        :rtype: Generator[str]
        """
        yield self._path
