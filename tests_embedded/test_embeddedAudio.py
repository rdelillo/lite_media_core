""" Test lite_media_core.media._embedded module.
"""
import unittest

from lite_media_core import media


class TestEmbeddedAudio(unittest.TestCase):
    """ Test lite_media_core.media._embedded module.
    """

    @classmethod
    def setUpClass(cls):
        """ Setup url.
        """
        super().setUpClass()
        cls.url = "https://www.myinstants.com/media/sounds/honteux_ACACNOH.mp3"
        cls.embedded_audio = media.EmbeddedAudio(cls.url)

    def test_valid_embedded(self):
        """ Ensure an embedded media can be created from a valid url.
        """
        self.assertIsInstance(self.embedded_audio, media.EmbeddedAudio)

    def test_invalid_embedded(self):
        """ Ensure an invalid embedded url raise an error.
        """
        with self.assertRaises(media.UnsupportedMimeType):
            _ = media.EmbeddedAudio("this_is_an_invalid_url")

    def test_settings(self):
        """ Ensure common settings can be gathered from the EmbeddedAudio object.
        """
        self.assertEqual(
            (
                1.056,
                "00:00:01:02",
                128000,
                48000,
            ),
            (
                self.embedded_audio.duration,
                str(self.embedded_audio.conformed_duration),
                self.embedded_audio.bitrate,
                self.embedded_audio.sampling_rate,
            )
        )
