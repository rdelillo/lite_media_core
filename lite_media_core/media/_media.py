""" Base media module.
"""
from typing import Union

import logging
import os

from lite_media_core.path_utils import sequence
from lite_media_core.path_utils import mime_types


class MediaException(Exception):
    """ Override exception for Media.
    """


class UnsupportedMimeType(ValueError):
    """ Overrides ValueError for mime-type mismatches.
    """


class Media:
    """ Generic media object.
    """

    def __init__(self, path: str, mime_type: str = None):
        """ Initialize a new Media object.
        """
        self._path = path

        if not mime_type:
            mime_types.reload_mimetypes()
            self._mime_type = mime_types.mimetypes.guess_type(self._path)[0]
        else:
            self._mime_type = mime_type

    def __str__(self) -> str:
        """ Represent current Media object as string.
        """
        online = "online" if self.exists else "offline"
        return (
            f"<{self.__class__.__name__} '{self.path}' "
            f"({self._mime_type}) {online}>"
        )

    def __repr__(self) -> str:
        """ Represent current Media object.

        :return: The object representation.
        :rtype: str
        """
        return (
            f"<{self.__class__.__name__} path='{self.path}' "
            f"(mimeType='{self._mime_type}')>"
        )

    def __iter__(self):
        """ Iterate over the media path(s).
        """
        yield self

    def __eq__(self, other: object) -> bool:
        """ Compare the Media object to another media object.

        :raises TypeError: If the other object is not a media object.
        """
        if not isinstance(other, Media):
            raise TypeError(f"Invalid comparison between 'Media' and {type(other).__name__}.")

        return self.path == other.path

    def __ne__(self, other: object) -> bool:
        """ Compare the Media object to another media object.
        """
        return not self == other

    def __hash__(self) -> int:
        """ Generate a hash value.
        """
        return hash(str(self.path))

    @property
    def path(self) -> str:
        """ The media file path.
        """
        return self._path

    @property
    def type(self) -> str:
        """ The media mime type.
        """
        mime_type, _ = _conform_mime_type(self._mime_type)
        return mime_type

    @property
    def sub_type(self) -> str:
        """
        :return: The media mime sub type.
        :rtype: str
        """
        _, mime_sub_type = _conform_mime_type(self._mime_type)
        return mime_sub_type

    @property
    def exists(self) -> bool:
        """ Is the current media reachable ?
        """
        return os.path.exists(self._path)

    @staticmethod
    def _raise_unsupported_media(path: str, mime_type: str = None):
        """ Raise for unsupported media path.

        :raise UnsupportedMimeType.
        """
        raise UnsupportedMimeType(f"Unsupported media path: {path}  type: {mime_type}.")

    @classmethod
    def from_path(cls, path: str):
        """ Create and returns a new Media object from a specific path.

        :raise ValueError: When the provided media path is not supported.
        """

        from lite_media_core.media._audio import Audio  # pylint: disable=C0415
        from lite_media_core.media._image import Image, ImageSequence  # pylint: disable=C0415
        from lite_media_core.media._video import Movie  # pylint: disable=C0415

        MEDIA_PER_MIME_TYPES = {"audio": Audio, "image": Image, "video": Movie}

        mime_types.reload_mimetypes()
        mime_type, _ = mime_types.mimetypes.guess_type(path)
        m_type, _ = _conform_mime_type(mime_type)

        try:
            seq_path = sequence.Sequence.from_string(path)

        except ValueError:
            seq_path = None

        # Need to create an ImageSequence ?
        if (
            seq_path is not None
            and (
                m_type in Image.registered_mime_types
                or mime_type is None
            )
        ):
            return ImageSequence(path)

        media_func = MEDIA_PER_MIME_TYPES.get(m_type, cls._raise_unsupported_media)
        return media_func(path, mime_type=mime_type)


def _conform_mime_type(mime_type: Union[str, None]) -> tuple:
    """ Conform a provided mime type string.
    """
    if not isinstance(mime_type, str):
        return None, None

    try:
        m_type, m_sub_type = mime_type.split("/")
        return m_type, m_sub_type

    except ValueError:
        return None, None
