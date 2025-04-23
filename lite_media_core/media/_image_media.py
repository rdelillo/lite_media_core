""" Image based media module.
"""
import lite_media_core.path_utils

from lite_media_core import _media_info
from lite_media_core.media import _media
from lite_media_core.path_utils import sequence as _sequence
from lite_media_core import resolution


class ImageMedia(_media.Media):
    """ Generic image based media.
    """

    registered_mime_types = ("application", "image", "video")

    def __init__(self, path: str, mime_type: str = None):
        """ Create an ImageMedia object.

        :raise UnsupportedMimeType: When the provided path is not an image based media.
        """
        super().__init__(path, mime_type=mime_type)

        if self.type not in ImageMedia.registered_mime_types:
            raise _media.UnsupportedMimeType(
                f"Cannot initialize ImageMedia from path {path} ({self._mime_type}) "
                f"valid types are {ImageMedia.registered_mime_types}."
            )

        # The information is computed on need, when a specific attribute is queried.
        self._info, self._metadata = None, None

    def _set_media_information(self):
        """ Helper, will update information and metadata dictionaries.
        """
        if self._info:  # Already gathered.
            return

        try:
            self._info, self._metadata = _media_info.get_media_information(self._path)

        except ValueError as error:
            raise _media.MediaException(f"Cannot get media information for {self}, offline ?") from error

    @property
    def resolution(self) -> resolution.Resolution:
        """ The media resolution.
        """
        self._set_media_information()
        return resolution.Resolution(
            self._info["width"],
            self._info["height"],
            pixel_aspect_ratio=self._info.get("pixelAspectRatio", 1.0),
        )

    @property
    def metadata(self) -> dict:
        """ The media metadata.
        """
        self._set_media_information()
        return self._metadata

    @property
    def frame_range(self) -> _sequence.FrameRange:
        """ The media frame range.
        """
        item = lite_media_core.path_utils.from_string(self.path)

        if isinstance(item, lite_media_core.path_utils.Sequence):
            return item.frame_range

        # default frame range
        return lite_media_core.path_utils.sequence.FrameRange(1, 1)
