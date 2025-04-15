""" Test lite_media_core.media._video module.
"""
import os
import unittest

import lite_media_core.path_utils

from lite_media_core import media
from lite_media_core import rate
from lite_media_core import timeCode


class TestMovie(unittest.TestCase):
    """ Test lite_media_core.media.Movie class.
    """
    def setUp(self):
        """ Initialize testing class.
        """
        super(TestMovie, self).setUp()

        mediaPath = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "media",
        )
        self.movie = media.Movie(os.path.join(mediaPath, "video.mov"))
        self.movieTc = media.Movie(os.path.join(mediaPath, "video_with_tc.mov"))

    def test_failsFromNotVideo(self):
        """ Ensure a Movie object fails when not created from a video file.
        """
        self.assertRaises(
            media.UnsupportedMimeType,
            media.Movie,
            "/path/to/an/image.jpg",
        )

    def test_codec(self):
        """ Ensure video codec can be retrieved from a video media.
        """
        self.assertEqual(
            ("MPEG-4 Visual", "ProRes"),
            (self.movie.codec, self.movieTc.codec),
        )

    def test_duration(self):
        """ Ensure duration can be retrieved from a video media.
        """
        expected1 = timeCode.TimeCode("00:00:00:01", 24)
        expected2 = timeCode.TimeCode("00:00:00:02", 24)

        self.assertEqual(
            (expected1, expected2),
            (self.movie.duration, self.movieTc.duration),
        )

    def test_frameRate(self):
        """ Ensure frame rate can be retrieved from a video media.
        """
        expected = rate.FrameRate(24)
        self.assertEqual(expected, self.movie.framerate)

    def test_timeCode_None(self):
        """ Ensure a Movie with no embedded timecode return None.
        """
        self.assertIsNone(self.movie.timeCode)

    def test_timeCode(self):
        """ Ensure an embedded timecode can be retrieved from a Movie.
        """
        expected = timeCode.TimeCode("01:02:03:04", 24)
        self.assertEqual(expected, self.movieTc.timeCode)

    def test_frameRange(self):
        """ Ensure a frame range can be retrieved from a Movie.
        """
        self.assertEqual(
            lite_media_core.path_utils.sequence.FrameRange(1, 1),
            self.movie.frameRange
        )

    def test_frameRange_embeddedTc(self):
        """ Ensure a frame range can be retrieved from a Movie embedding a timecode.
        """
        self.assertEqual(
            lite_media_core.path_utils.sequence.FrameRange(89356, 89357),
            self.movieTc.frameRange
        )
