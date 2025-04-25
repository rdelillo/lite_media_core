""" Test lite_media_core.media._video module.
"""
import os
import unittest

from lite_media_core import path_utils
from lite_media_core import media
from lite_media_core import rate
from lite_media_core import timecode


class TestMovie(unittest.TestCase):
    """ Test lite_media_core.media.Movie class.
    """

    def setUp(self):
        """ Initialize testing class.
        """
        media_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "media",
        )
        self.movie = media.Movie(os.path.join(media_path, "video.mov"))
        self.movie_tc = media.Movie(os.path.join(media_path, "video_with_tc.mov"))

    def test_not_from_video(self):
        """ Ensure a Movie object fails when not created from a video file.
        """
        with self.assertRaises(media.UnsupportedMimeType):
            _ = media.Movie("/path/to/an/image.jpg")

    def test_codec(self):
        """ Ensure video codec can be retrieved from a video media.
        """
        self.assertEqual(
            ("MPEG-4 Visual", "ProRes"),
            (self.movie.codec, self.movie_tc.codec),
        )

    def test_duration(self):
        """ Ensure duration can be retrieved from a video media.
        """
        expected1 = timecode.Timecode("00:00:00:01", 24)
        expected2 = timecode.Timecode("00:00:00:02", 24)

        self.assertEqual(
            (expected1, expected2),
            (self.movie.duration, self.movie_tc.duration),
        )

    def test_frameRate(self):
        """ Ensure frame rate can be retrieved from a video media.
        """
        expected = rate.FrameRate(24)
        self.assertEqual(expected, self.movie.framerate)

    def test_timecode_None(self):
        """ Ensure a Movie with no embedded timecode return None.
        """
        self.assertIsNone(self.movie.timecode)

    def test_timecode(self):
        """ Ensure an embedded timecode can be retrieved from a Movie.
        """
        expected = timecode.Timecode("01:02:03:04", 24)
        self.assertEqual(expected, self.movie_tc.timecode)

    def test_frameRange(self):
        """ Ensure a frame range can be retrieved from a Movie.
        """
        self.assertEqual(
            path_utils.sequence.FrameRange(1, 1),
            self.movie.frame_range
        )

    def test_frameRange_embeddedTc(self):
        """ Ensure a frame range can be retrieved from a Movie embedding a timecode.
        """
        self.assertEqual(
            path_utils.sequence.FrameRange(89356, 89357),
            self.movie_tc.frame_range
        )
