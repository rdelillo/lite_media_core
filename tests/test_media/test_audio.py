""" Test lite_media_core.media._audio module.
"""
import unittest
import os

from lite_media_core import media


mediaPath = _mediaPath = os.path.join(
    os.path.dirname(__file__),
    "..",
    "resources",
    "media",
)


class TestMedia(unittest.TestCase):
    """ Test lite_media_core.media.Audio class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setup class.
        """
        super().setUpClass()
        cls.audioFile = os.path.join(mediaPath, "sample.mp3")
        cls.audioSample = media.Audio.fromPath(cls.audioFile)

    def test_failsFromNotAnAudio(self):
        """ Ensure an Audio object fails when not created from an audio file.
        """
        self.assertRaises(
            ValueError,
            media.Audio,
            "/path/to/an/image.jpg",
        )

    def test_audio_mp3(self):
        """ Ensure an Audio object can be created from an mp3.
        """
        self.assertIsInstance(self.audioSample, media.Audio)
        self.assertTrue(self.audioSample.exists)
        self.assertEqual(
            ("audio", "mpeg3"),
            (self.audioSample.type, self.audioSample.subType),
        )

    def test_audio_settings(self):
        """ Ensure basic settings of an audio file can be sorted.
        """
        self.assertEqual(
            (
                0.456,
                "00:00:00:11",
                128000,
                48000,
            ),
            (
                self.audioSample.duration,
                str(self.audioSample.conformedDuration),
                self.audioSample.bitrate,
                self.audioSample.samplingRate
            )
        )

    def test_longer_audio_settings(self):
        """ Ensure basic settings of an audio file can be sorted.
        """
        audioFile = os.path.join(mediaPath, "sample2.mp3")
        audioSample = media.Audio.fromPath(audioFile)

        self.assertEqual(
            (
                7,
                "00:00:07:06",
                64000,
                44100,
            ),
            (
                int(audioSample.duration),
                str(audioSample.conformedDuration),
                audioSample.bitrate,
                audioSample.samplingRate
            )
        )
