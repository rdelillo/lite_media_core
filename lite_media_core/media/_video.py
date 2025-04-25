""" Video module.
"""
from typing import Optional

from lite_media_core.media import _image_media
from lite_media_core.media import UnsupportedMimeType
from lite_media_core.path_utils import sequence
from lite_media_core import rate
from lite_media_core import timecode


class Movie(_image_media.ImageMedia):
    """ Movie media.
    """

    registered_mime_types = ("video", "application/mxf")

    def __init__(self, path: str, mime_type: str = None):
        """ Initialize a new Movie object.

        :raise UnsupportedMimeType: When the provided path is not a video media.
        """
        super().__init__(path, mime_type=mime_type)

        if (
            self.type not in Movie.registered_mime_types
            and self._mime_type not in Movie.registered_mime_types
        ):
            raise UnsupportedMimeType(
                f"Cannot create a Movie media from {path} ({self.type}) "
                f"valid types are {Movie.registered_mime_types}."
            )

    @property
    def codec(self) -> str:
        """ The video codec.
        """
        self._set_media_information()
        return self._info["codec"]

    @property
    def framerate(self) -> rate.FrameRate:
        """ The movie frame rate.
        """
        return self.duration.frame_rate

    @property
    def duration(self) -> timecode.Timecode:
        """ The movie duration.
        """
        self._set_media_information()
        tcIn = int(self._info['frames']) if self._info['frames'] else self._info['duration']
        return timecode.Timecode(tcIn, self._info["frameRate"])

    @property
    def timecode(self) -> Optional[timecode.Timecode]:
        """ An embedded timecode in the Movie or None.
        """
        self._set_media_information()
        if self._info.get("timecode"):
            frameRate = self._info.get("tcFrameRate") or self._info["frameRate"]
            return timecode.Timecode(self._info["timecode"], frameRate)

        return None

    @property
    def frame_range(self) -> sequence.FrameRange:
        """ The video frame range.
        """
        start_tc = self.timecode or 1  # default frame is 1
        return sequence.FrameRange(
            int(start_tc),
            int(start_tc) + int(self.duration) - 1,
        )
