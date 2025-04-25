""" Audio module.
"""
from lite_media_core import timecode as _timecode
from lite_media_core import _media_info
from lite_media_core.media import _media


class Audio(_media.Media):
    """ Audio media.
    """
    registered_mime_types = ("audio",)

    def __init__(self, path: str, mime_type: str = None):
        """ Initialize a new Audio object.

        :raise ValueError: When the provided path is not an audio media.
        """
        super().__init__(path, mime_type=mime_type)

        if self.type != "audio":
            raise _media.UnsupportedMimeType(
                f"Cannot create an Audio media from {path} ({self.type}) "
                f"valid types are {Audio.registered_mime_types}."
            )

        # Delay information load.
        # The information is computed on need, when audio attribute is queried.
        self._info, self._metadata = None, None

    def _set_media_information(self):
        """ Gather audio file information.

        :raise: `lite_media_core.MediaException`: When no information can be gathered from the media.
        """
        if self._info is not None:
            return

        try:
            self._info, self._metadata = _media_info.get_media_information(self._path)

        except ValueError as error:
            raise _media.MediaException(f"Cannot get media information for {self}, offline ?") from error

    @property
    def duration(self) -> float:
        """ The audio duration in seconds.
        """
        self._set_media_information()
        return self._info["duration_in_ms"] / 1000.0

    @property
    def conformed_duration(self) -> _timecode.Timecode:
        """ The audio duration as timecode (24fps).
        """
        self._set_media_information()
        return _timecode.Timecode.from_seconds(
            self.duration,
            24.0,
        )

    @property
    def sampling_rate(self) -> int:
        """ The audio sampling rate.
        """
        self._set_media_information()
        return self._info["samplingRate"]

    @property
    def bitrate(self) -> int:
        """ The audio bitrate.
        """
        self._set_media_information()
        return self._info["bitrate"]

    @property
    def metadata(self) -> dict:
        """ The metadata associated with the audio file.
        """
        self._setMediaInformation()
        return self._metadata.copy()
