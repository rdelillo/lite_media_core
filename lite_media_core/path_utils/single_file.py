""" Single file object.
"""
import os

from typing import Union

from lite_media_core.path_utils import sequence


class SingleFile:
    """ A SingleFile object represent an individual unpadded file.
    """

    def __init__(self, path: str):
        """ Initialize the SingleFile.
        """
        self._path = path

    def __eq__(self, other: Union[sequence.Sequence]) -> bool:
        """ Is equal ?
        """
        if isinstance(other, sequence.Sequence):
            return os.path.abspath(self._path) == other.start == other.end

        return repr(self) == repr(other)

    def __ne__(self, other: Union[sequence.Sequence]) -> bool:
        """ Is not equal ?
        """
        return repr(self) != repr(other)

    def __hash__(self) -> int:
        """ Hash representation.
        """
        return hash(repr(self))

    def __repr__(self) -> str:
        """ The representation of the SingleFile.
        """
        return f"<{self.__class__.__name__} {self._path}>"

    def __str__(self) -> str:
        """ The string representation of the SingleFile.
        """
        return self._path

    def __iter__(self) -> list:
        """ Iterate over the path of the SingleFile.
        """
        yield self._path
