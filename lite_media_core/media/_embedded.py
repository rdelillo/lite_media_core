""" Embedded module.
"""
import contextlib
import os
import importlib
import tempfile
import sys

from importlib import utils as _impt_utils
from typing import Optional

from lite_media_core import rate as _rate
from lite_media_core import resolution as _resolution
from lite_media_core import timeCode as _timeCode
from lite_media_core.path_utils import sequence as _sequence
from lite_media_core.media import _media
from lite_media_core.media import _audio

# Ensure lite_media_core was installed with the
# "embedded_media" extra requires. We do not want
# those dependencies most of the time.

if _impt_utils.find_spec("yt_dlp"):
    requests = importlib.import_module("requests")
    validators = importlib.import_module("validators")
    yt_dlp = importlib.import_module("yt_dlp")
    _IS_IMPORTED = True

else:
    _IS_IMPORTED = False

class UnsupportedUrl(_media.UnsupportedMimeType):
    """ Overrides UnsupportedMimeType for URL issues.
    """


@contextlib.contextmanager
def _all_print_disabled():
    """
    A context manager that will prevent any print messages
    triggered during the body from being processed.
    """
    previous_out = sys.stdout
    previous_err = sys.stderr

    sys.stdout = open(os.devnull, "w")  #pylint: disable=W1514
    sys.stderr = open(os.devnull, "w")  #pylint: disable=W1514

    try:
        yield

    finally:
        sys.stdout = previous_out
        sys.stderr = previous_err


class EmbeddedMedia(_media.Media):
    """ Embedded media contained on an URL page.
    """

    def __init__(self, url: str, mime_type: str = None):
        """ Initialize a new Embedded object.

        :raise UnsupportedMimeType: When the provided path is not a video media.
        """
        self._check_available()
        if not validators.url(url):
            raise _media.UnsupportedMimeType(
                f'Cannot create an EmbeddedMedia from invalid url: {url}.'
            )

        super().__init__(url, mime_type=mime_type)

    @classmethod
    def _check_available(cls):
        """
            :raise RuntimeError: When the requirements for embedded are not found.
        """
        if not _IS_IMPORTED:
            raise RuntimeError(
                f"Cannot create a {cls} media, ensure that lite_media_core "
                "is installed with the 'embedded_media' extra requires."
            )


class EmbeddedAudio(EmbeddedMedia):
    """ Embedded audio stored on a server.
    """

    def __init__(self, url: str, mime_type: str = None):
        """ Initialize a new EmbeddedAudio object.

        :raise UnsupportedMimeType: When the provided path is not a video media.
        """
        self._audio_proxy = None
        super().__init__(url, mime_type=mime_type)

        # Delay information load.
        # The information is computed on need, when a specific attribute is queried.
        self._info, self._metadata = None, None

        if self.type != "audio":
            raise _media.UnsupportedMimeType(
                f"Cannot create an Audio media from {url} ({self.type}) "
                f"valid types are {_audio.Audio.registered_mime_types}."
            )

    def __del__(self):
        """ Ensure generated proxy is removed on delete.
        """
        if self._audio_proxy:
            os.remove(self._audio_proxy.path)

        del self

    def _download_proxy(self) -> Optional[_audio.Audio]:
        """
        :return: An audio proxy.
        :rtype: :class:`lite_media_core.media.Audio` or None
        """
        try:
            doc = requests.get(self.path, timeout=60)
            _, ext = os.path.splitext(self.path)
            temporary_proxy = os.path.join(tempfile.mkdtemp(), "sample" + ext)
            with open(temporary_proxy, "wb") as fHandler:
                fHandler.write(doc.content)

            return temporary_proxy

        except Exception as error:
            raise _media.MediaException(f"Cannot generate audio proxy for {self}.") from error

    def _get_proxy_information(self):
        """ Gather audio information from the proxy.
        """
        if self._audio_proxy is not None:
            return

        proxy_path = self._download_proxy()
        self._audio_proxy = _audio.Audio.from_path(proxy_path)

    @property
    def duration(self) -> float:
        """ The audio file duration in seconds.
        """
        self._get_proxy_information()
        return self._audio_proxy.duration

    @property
    def conformed_duration(self) -> _timeCode.TimeCode:
        """ The audio file conformed duration as timecode (24fps).
        """
        self._get_proxy_information()
        return self._audio_proxy.conformed_duration

    @property
    def sampling_rate(self) -> int:
        """ The audio file sampling rate.
        """
        self._get_proxy_information()
        return self._audio_proxy.sampling_rate

    @property
    def bitrate(self) -> int:
        """ The audio file bitrate.
        """
        self._get_proxy_information()
        return self._audio_proxy.bitrate



class EmbeddedVideo(EmbeddedMedia):
    """ Embedded video contained on an URL page.
    """

    def __init__(
        self,
        url: str,
        mime_type: str = None,
        full_extraction: bool = True,
        use_proxy: bool = False
    ):
        """ Initialize a new Embedded object.

        :raise UnsupportedMimeType: When the provided path is not a video media.
        """
        self._check_available()
        options = {
            "playlist_items": "1",
            "color": {"stderr": "no_color", "stdout": "no_color"},
        }

        if use_proxy:
            options["proxy"] = "socks5://dante_user:dante_user@45.91.251.124:1080/"

        with _all_print_disabled():
            try:
                data = yt_dlp.YoutubeDL(options).extract_info(url, process=full_extraction, download=False)

            except yt_dlp.DownloadError as error:
                raise UnsupportedUrl(str(error)) from error

            except Exception as error:
                raise RuntimeError from error

        # Handle playlist
        if data.get("_type") == "playlist":
            try:
                data = data["entries"][0] # full processed info
            except TypeError:
                data = next(data["entries"])  # partial extracted info

        self._settings = dict(data)
        _ = str(self._settings) # force expand otherwise not picklable cause contain generator.

        mime_type = 'video/' + self._settings.get('extractor', 'unknown')
        _media.Media.__init__(self, url, mime_type=mime_type)  #pylint: disable=W0233

    @property
    def codec(self) -> str:
        """ The EmbeddedVideo video codec.
        """
        return self._settings['vcodec']

    @property
    def resolution(self) -> _resolution.Resolution:
        """ The EmbeddedVideo resolution.
        """
        return _resolution.Resolution(
            self._settings['width'],
            self._settings['height']
        )

    @property
    def framerate(self) -> _rate.FrameRate:
        """ The EmbeddedVideo frame rate.
        """
        return _rate.FrameRate.from_custom_rate(self._settings.get('fps', 24.0))

    @property
    def framerange(self) -> _sequence.FrameRange:
        """ The EmbeddedVideo frameRange.
        """
        return _sequence.FrameRange(1, int(self.duration) - 1)

    @property
    def duration(self) -> _timeCode.TimeCode:
        """ The EmbeddedVideo duration.
        """
        return _timeCode.TimeCode.from_seconds(
            self._settings['duration'],
            self._settings.get('fps', 24)
        )

    @property
    def metadata(self) -> dict:
        """ The EmbeddedVideo metadata.
        """
        return self._settings.copy()
