""" Test lite_media_core.media._embedded module.
"""
import unittest

from importlib import utils as _impt_utils

from lite_media_core import media


class TestEmbeddedMedia(unittest.TestCase):
    """ Test lite_media_core.media._embedded media.
    """

    def test_embedded_video(self):
        """ Ensure an embedded video is available only if extra requirement is correctly set.
        """
        if not _impt_utils.find_spec("yt_dlp"):
            with self.assertRaises(RuntimeError):
                 _ = media.EmbeddedVideo("")

    def test_embedded_audio(self):
        """ Ensure an embedded audio is available only if extra requirement is correctly set.
        """
        if not _impt_utils.find_spec("yt_dlp"):
            with self.assertRaises(RuntimeError):
                _ = media.EmbeddedAudio("")
