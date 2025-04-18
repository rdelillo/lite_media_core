""" Test lite_media_core.media._embedded module.
"""
import os
import unittest

from lite_media_core import media


class TestEmbeddedMedia(unittest.TestCase):
    """ Test lite_media_core.media._embedded media.
    """

    def test_embedded_video(self):
        """ Ensure an embedded video is available only if extra requirement is correctly set.
        """
        try:
            import yt_dlp

        except ModuleNotFoundError:
            with self.assertRaises(RuntimeError):
                _ = media.EmbeddedVideo("")

    def test_embedded_audio(self):
        """ Ensure an embedded audio is available only if extra requirement is correctly set.
        """
        try:
            import yt_dlp

        except ModuleNotFoundError:
            with self.assertRaises(RuntimeError):
                _ = media.EmbeddedAudio("")
