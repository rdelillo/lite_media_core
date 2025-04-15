""" Image based media module.
"""
import lite_media_core.path_utils

from lite_media_core import _mediaInfo
from lite_media_core.media import _media
from lite_media_core import resolution


class ImageMedia(_media.Media):
    """ Generic image based media.
    """
    registeredMimeTypes = ("application", "image", "video")

    def __init__(self, path, mimeType=None):
        """ Create an ImageMedia object.

        :param str path: The media file path.
        :param str mimeType: An optional media mime-type.
        :raise UnsupportedMimeType: When the provided path is not an image based media.
        """
        super().__init__(path, mimeType=mimeType)

        if self.type not in ImageMedia.registeredMimeTypes:
            raise _media.UnsupportedMimeType("Cannot initialize ImageMedia from path %s (%s) "
                "valid types are %s." % (path, self._mimeType, ImageMedia.registeredMimeTypes))

        # Delay information load.
        # Gathering information from a specific media can be time-consuming (or even not possible
        # when the media does not exist). However, users should still be able to create media objects
        # skipping this step.
        # The information is then computed on need, when specific attributes are queried.
        self._info, self._metadata = None, None

    def _setMediaInformation(self):
        """ Helper, will update information and metadata dictionaries.
        """
        if self._info:  # Already gathered.
            return

        try:
            self._info, self._metadata = _mediaInfo.getMediaInformation(self._path)

        except ValueError as error:
            raise _media.MediaException("Cannot get media information for %s, offline ?" % self) from error

    @property
    def resolution(self):
        """
        :return: The media resolution.
        :rtype: :class:`lite_media_core.resolution.Resolution`
        """
        self._setMediaInformation()
        return resolution.Resolution(
            self._info["width"],
            self._info["height"],
            pixelAspectRatio=self._info.get("pixelAspectRatio", 1.0),
        )

    @property
    def metadata(self):
        """
        :return: The media metadata.
        :rtype: dict
        """
        self._setMediaInformation()
        return self._metadata

    @property
    def frameRange(self):
        """
        :return: The media frame range.
        :rtype: :class:`lite_media_core.path_utils.sequence.FrameRange`
        """
        item = lite_media_core.path_utils.fromString(self.path)

        if isinstance(item, lite_media_core.path_utils.Sequence):
            return item.frameRange

        return lite_media_core.path_utils.sequence.FrameRange(1, 1)
