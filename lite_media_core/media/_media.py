""" Base media module.
"""
import logging
import os

from lite_media_core.path_utils import sequence
from lite_media_core.path_utils import mimeTypes


class MediaException(Exception):
    """ Override exception for Media.
    """


class UnsupportedMimeType(ValueError):
    """ Overrides ValueError for mime-type mismatches.
    """


class Media:
    """ Generic media object.
    """
    def __init__(self, path, mimeType=None):
        """ Initialize a new Media object.

        :param str path: The media file path.
        :param str mimeType: An optional media mime-type.
        """
        self._path = path

        if not mimeType:
            mimeTypes.reload_mimetypes()
            self._mimeType = mimeTypes.mimetypes.guess_type(self._path)[0]
        else:
            self._mimeType = mimeType

    def __str__(self):
        """ Represent current Media object as string.

        :return: The string representation.
        :rtype: str
        """
        return "<%s %r (%s) %s>" % (
            self.__class__.__name__,
            self.path,
            self._mimeType,
            "online" if self.exists else "offline",
        )

    def __repr__(self):
        """ Represent current Media object.

        :return: The object representation.
        :rtype: str
        """
        return "<%s path='%s' (mimeType=%r)>" % (
            self.__class__.__name__,
            self.path,
            self._mimeType,
        )

    def __iter__(self):
        """ Iterate over the media path(s).

        :rtype: Generator[:class:`Media`]
        """
        yield self

    def __eq__(self, other):
        """ Compare the Media object to another media object.

        :param other: A media object.
        :type other: :class:`lite_media_core.media.Media`
        :return: If the other media object the same?
        :rtype: bool
        :raises TypeError: If the other object is not a media object.
        """
        if not isinstance(other, Media):
            raise TypeError("Invalid comparison between 'Media' and %r." % type(other).__name__)
        return self.path == other.path

    def __ne__(self, other):
        """ Compare the Media object to another media object.

        :param other: A media object.
        :type other: :class:`lite_media_core.media.Media`
        :return: Is the other media object different?
        :rtype: bool
        """
        return not self == other

    def __hash__(self):
        """ Generate a hash.

        :return: A hash value.
        :rtype int
        """
        return hash(str(self.path))

    @property
    def path(self):
        """
        :return: The media file path.
        :rtype: str
        """
        return self._path

    @property
    def type(self):
        """
        :return: The media mime type.
        :rtype: str
        """
        mimeType, _ = _conformMimeType(self._mimeType)
        return mimeType

    @property
    def subType(self):
        """
        :return: The media mime sub type.
        :rtype: str
        """
        _, mimeSubType = _conformMimeType(self._mimeType)
        return mimeSubType

    @property
    def exists(self):
        """
        :return: Is the current media object on disk ?
        :rtype: bool
        """
        return os.path.exists(self._path)

    @classmethod
    def fromPath(cls, path):
        """ Create and returns a new Media object from a specific path.

        :param str path: The media file path.
        :return: The media object.
        :rtype: :class:`Media`
        :raise ValueError: When the provided media path is not supported.
        """
        # Prevent recursive imports
        from lite_media_core.media._audio import Audio  # pylint: disable=C0415
        from lite_media_core.media._image import Image, ImageSequence  # pylint: disable=C0415
        from lite_media_core.media._video import Movie  # pylint: disable=C0415

        mimeTypes.reload_mimetypes()
        mimeType, _ = mimeTypes.mimetypes.guess_type(path)
        mType, _ = _conformMimeType(mimeType)

        # If the input path is a sequence, try to create an ImageSequence object.
        try:
            seqPath = sequence.Sequence.fromString(path)

        except ValueError:
            seqPath = None

        if isinstance(seqPath, sequence.Sequence) and (
            mType in Image.registeredMimeTypes or
            mimeType is None
        ):
            return ImageSequence(path)

        # Special triage for Movie special mime-types
        # e.g. 'application/mxf'.
        if mimeType in Movie.registeredMimeTypes:
            return Movie(path, mimeType=mimeType)

        mediaMimeTypes = {"audio": Audio, "image": Image, "video": Movie}
        return mediaMimeTypes.get(mType, _raiseUnsupportedMedia)(path, mimeType=mimeType)


def _raiseUnsupportedMedia(path, mimeType=None):
    """ Unsupported media path.

    :param str path: The media path.
    :param str mimeType: An optional mimeType.
    :raise UnsupportedMimeType:
    """
    raise UnsupportedMimeType("Unsupported media path: %r  type: %r." % (path, mimeType))


def _conformMimeType(mimeType):
    """ Conform a provided mime type string.

    :param object mimeType: An object which can translate as a mime type string.
    :return: The conformed media mime type and subType (None if not valid).
    :rtype: tuple.
    """
    if not isinstance(mimeType, (str, type(None))):
        logging.error("Cannot conform invalid mimeType: %r.", mimeType)

    try:
        mType, mSubType = mimeType.split("/")
        return mType, mSubType

    except (AttributeError, ValueError):
        return None, None
