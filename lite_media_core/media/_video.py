""" Video module.
"""
import lite_media_core.path_utils

from lite_media_core.media import _imageMedia
from lite_media_core.media import UnsupportedMimeType
from lite_media_core import timeCode


class Movie(_imageMedia.ImageMedia):
    """ Movie media.
    """
    registeredMimeTypes = ("video", "application/mxf")

    def __init__(self, path, mimeType=None):
        """ Initialize a new Movie object.

        :param str path: The media file path.
        :param str mimeType: An optional media mime-type.
        :raise UnsupportedMimeType: When the provided path is not a video media.
        """
        super().__init__(path, mimeType=mimeType)

        if self.type not in Movie.registeredMimeTypes and self._mimeType not in Movie.registeredMimeTypes:
            raise UnsupportedMimeType("Cannot create a Movie media from %s (%s) "
                "valid types are %s." % (path, self.type, Movie.registeredMimeTypes))

    @property
    def codec(self):
        """
        :return: The video codec.
        :rtype: str
        """
        self._setMediaInformation()
        return self._info["codec"]

    @property
    def framerate(self):
        """
        :return: The movie frame rate.
        :rtype: :class:`lite_media_core.rate.FrameRate`
        """
        return self.duration.frameRate

    @property
    def duration(self):
        """
        :return: The movie frame count duration.
        :rtype: :class:`lite_media_core.timeCode.TimeCode`
        """
        self._setMediaInformation()
        tcIn = int(self._info['frames']) if self._info['frames'] else self._info['duration']
        return timeCode.TimeCode(tcIn, self._info["frameRate"])

    @property
    def timeCode(self):
        """
        :return: An embedded timecode in the Movie or None.
        :rtype: :class:`lite_media_core.timeCode.TimeCode`
        """
        self._setMediaInformation()
        if self._info.get("timecode"):
            frameRate = self._info.get("tcFrameRate") or self._info["frameRate"]
            return timeCode.TimeCode(self._info["timecode"], frameRate)

        return None

    @property
    def frameRange(self):
        """
        :return: The video frame range.
        :rtype: :class:`lite_media_core.path_utils.sequence.FrameRange`
        """
        startTc = self.timeCode or 1  # default frame is 1
        return lite_media_core.path_utils.sequence.FrameRange(
            int(startTc),
            int(startTc) + int(self.duration) - 1,  # 3 frames = 1-3
        )
