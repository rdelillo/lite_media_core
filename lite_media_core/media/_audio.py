""" Audio module.
"""
from lite_media_core import timeCode as _timeCode
from lite_media_core import _mediaInfo
from lite_media_core.media import _media


class Audio(_media.Media):
    """ Audio media.
    """
    registeredMimeTypes = ("audio",)

    def __init__(self, path, mimeType=None):
        """ Initialize a new Audio object.

        :param str path: The media file path.
        :param str mimeType: An optional media mime-type.
        :raise ValueError: When the provided path is not an audio media.
        """
        super().__init__(path, mimeType=mimeType)

        if self.type != "audio":
            raise _media.UnsupportedMimeType("Cannot create an Audio media from %s (%s) "
                 "valid types are %s." % (path, self.type, Audio.registeredMimeTypes))

        # Delay information load.
        # Gathering information from a specific media can be time-consuming (or even not possible
        # when the media does not exist). However, users should still be able to create media objects
        # skipping this step.
        # The information is then computed on need, when specific attributes are queried.
        self._info, self._metadata = None, None

    def _setMediaInformation(self):
        """ Gather audio file information.

        :raise: `lite_media_core.MediaException`: When no information can be gathered from the media.
        """
        if self._info is not None:
            return

        try:
            self._info, self._metadata = _mediaInfo.getMediaInformation(self._path)

        except ValueError as error:
            raise _media.MediaException("Cannot get media information for %s, offline ?" % self) from error

    @property
    def duration(self):
        """ The audio duration.

        :return: The audio file duration.
        :rtype: float
        """
        self._setMediaInformation()
        return self._info["duration_in_ms"] / 1000.0

    @property
    def conformedDuration(self):
        """ The audio duration.

        :return: The audio file duration.
        :rtype: `class:lite_media_core.timeCode.Timecode`
        """
        self._setMediaInformation()
        return _timeCode.TimeCode.fromSeconds(
            self.duration,
            24.0,
        )

    @property
    def samplingRate(self):
        """
        :return: The audio sampling rate.
        :rtype: int
        """
        self._setMediaInformation()
        return self._info["samplingRate"]

    @property
    def bitrate(self):
        """
        :return: The audio file bitrate.
        :rtype: int
        """
        self._setMediaInformation()
        return self._info["bitrate"]

    @property
    def metadata(self):
        """
        :return: The metadata associated with the audio file.
        :rtype: dict.
        """
        self._setMediaInformation()
        return self._metadata.copy()
