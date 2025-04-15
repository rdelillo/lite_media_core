""" Embedded module.
"""
import contextlib
import os
import tempfile
import sys

import requests
import validators
import yt_dlp

from lite_media_core import rate as _rate
from lite_media_core import resolution as _resolution
from lite_media_core import timeCode as _timeCode
from lite_media_core.path_utils import sequence as _sequence
from lite_media_core.media import _media
from lite_media_core.media import _audio


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

    def __init__(self, url, mimeType=None):
        """ Initialize a new Embedded object.

            :param str path: The media url.
            :param str mimeType: An optional media mime-type.
            :raise UnsupportedMimeType: When the provided path is not a video media.
        """
        if not validators.url(url):
            raise _media.UnsupportedMimeType(
                'Cannot create an EmbeddedMedia from invalid url: %r'
                % url)

        super().__init__(url, mimeType=mimeType)


class EmbeddedAudio(EmbeddedMedia):
    """ Embedded audio stored on a server.
    """

    def __init__(self, url, mimeType=None):
        """ Initialize a new Embedded object.

            :param str path: The media url.
            :param str mimeType: An optional media mime-type.
            :raise UnsupportedMimeType: When the provided path is not a video media.
        """
        self._audioProxy = None
        super().__init__(url, mimeType=mimeType)

        # Delay information load.
        # Gathering information from a specific media can be time-consuming (or even not possible
        # when the media does not exist). However, users should still be able to create media objects
        # skipping this step.
        # The information is then computed on need, when specific attributes are queried.
        self._info, self._metadata = None, None

        if self.type != "audio":
            raise _media.UnsupportedMimeType("Cannot create an Audio media from %s (%s) "
                 "valid types are %s." % (url, self.type, _audio.Audio.registeredMimeTypes))

    def __del__(self):
        """ Ensure generated proxy is removed on delete.
        """
        if self._audioProxy:
            os.remove(self._audioProxy.path)

        del self

    def _downloadProxy(self):
        """
        :return: An audio proxy.
        :rtype: :class:`lite_media_core.media.Audio` or None
        """
        try:
            doc = requests.get(self.path, timeout=60)
            _, ext = os.path.splitext(self.path)
            temporaryProxy = os.path.join(tempfile.mkdtemp(), "sample" + ext)
            with open(temporaryProxy, "wb") as fHandler:
                fHandler.write(doc.content)

            return temporaryProxy

        except Exception as error:
            raise _media.MediaException("Cannot generate audio proxy for %s" % self) from error

    def _getProxyInformation(self):
        """ Gather audio information form the proxy
        """
        if self._audioProxy is not None:
            return

        proxyPath = self._downloadProxy()
        self._audioProxy = _audio.Audio.fromPath(proxyPath)

    @property
    def duration(self):
        """
        :return: The audio file duration.
        :rtype: float
        """
        self._getProxyInformation()
        return self._audioProxy.duration

    @property
    def conformedDuration(self):
        """
        :return: The audio file conformed duration.
        :rtype: `class:lite_media_core.timeCode.Timecode`
        """
        self._getProxyInformation()
        return self._audioProxy.conformedDuration

    @property
    def samplingRate(self):
        """
        :return: The audio file sampling rate.
        :rtype: int
        """
        self._getProxyInformation()
        return self._audioProxy.samplingRate

    @property
    def bitrate(self):
        """
        :return: The audio file bitrate.
        :rtype: int
        """
        self._getProxyInformation()
        return self._audioProxy.bitrate



class EmbeddedVideo(EmbeddedMedia):
    """ Embedded video contained on an URL page.
    """

    def __init__(self, url, mimeType=None, full_extraction=True, use_proxy=False):  #pylint: disable=W0231
        """ Initialize a new Embedded object.

            :param str path: The media url.
            :param str mimeType: An optional media mime-type.
            :param bool full_extraction: Should it perform a full extraction.
            :param bool use_proxy: Shall it use the proxy or not.
            :raise UnsupportedMimeType: When the provided path is not a video media.
        """
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

        mimeType = 'video/' + self._settings.get('extractor', 'unknown')
        _media.Media.__init__(self, url, mimeType=mimeType)  #pylint: disable=W0233

    @property
    def codec(self):
        """ The EmbeddedVideo video codec.

        :return: The codec.
        :rtype: str
        """
        return self._settings['vcodec']

    @property
    def resolution(self):
        """ The EmbeddedVideo resolution.

        :return: The resolution.
        :rtype: :class:`lite_media_core.resolution.Resolution`
        """
        return _resolution.Resolution(
            self._settings['width'],
            self._settings['height']
        )

    @property
    def framerate(self):
        """ The EmbeddedVideo frame rate.

        :return: The frame rate.
        :rtype: :class:`lite_media_core.rate.FrameRate`
        """
        return _rate.FrameRate.fromCustomRate(self._settings.get('fps',24))

    @property
    def framerange(self):
        """ The EmbeddedVideo frameRange.

        :return: The framerange.
        :rtype: :class:`lite_media_core.path_utils.FrameRange`
        """
        return _sequence.FrameRange(1, int(self.duration) - 1)  # 3 frames = 1-3

    @property
    def duration(self):
        """ The EmbeddedVideo duration.

        :return: The duration.
        :rtype: :class:`lite_media_core.timeCode.Timecode`
        """
        return _timeCode.TimeCode.fromSeconds(
            self._settings['duration'],
            self._settings.get('fps', 24)
        )

    @property
    def metadata(self):
        """ The EmbeddedVideo metadata.

        :return: The embedded video metadata.
        :rtype: dict
        """
        return self._settings.copy()
