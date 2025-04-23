""" Test lite_media_core.media._image_media module.
"""
import os
import tempfile
import platform
import unittest

import mock

import lite_media_core.path_utils

from lite_media_core import media
from lite_media_core.media import _image_media
from lite_media_core import resolution


mediaPath = _mediaPath = os.path.join(
    os.path.dirname(__file__),
    "..",
    "resources",
    "media",
)


class TestImageMedia(unittest.TestCase):
    """ Test the generic ImageMedia class (image, movie...).
    """
    def setUp(self):
        """ Set up the testing class.
        """
        super().setUp()

        img_path = os.path.join(mediaPath, "img.png")
        self.imgMedia = _image_media.ImageMedia(img_path)

    def test_resolution(self):
        """ Ensure the resolution parameter is properly read from an ImageMedia object.
        """
        expected = resolution.Resolution(64, 64)
        self.assertEqual(expected, self.imgMedia.resolution)

    def test_resolutionAnamorphic(self):
        """ Ensure an anamorphic resolution is properly read from an ImageMedia object.
        """
        expected = resolution.Resolution(64, 64, pixel_aspect_ratio=2.0)
        ana_path = os.path.join(mediaPath, "img-anamorphic.exr")
        imgMedia = _image_media.ImageMedia(ana_path)

        self.assertEqual(expected, imgMedia.resolution)

    def test_metadata(self):
        """ Ensure the metadata can be retrieved from an ImageMedia object.
        """
        self.assertTrue(self.imgMedia.metadata)

    def test_delayLoad(self):
        """ Ensure media information gathering is delayed for an ImageMedia.
        """
        media_obj = _image_media.ImageMedia("/path/to/an/image.png")
        self.assertEqual(
            (None, None),
            (media_obj._info, media_obj._metadata),  # pylint: disable=W0212
        )

    def test_init_fails(self):
        """ Ensure an ImageMedia object cannot be created from an unsupported format.
        """
        with self.assertRaises(media.UnsupportedMimeType):
            _ = _image_media.ImageMedia("/path/to/an/audio.wav")

    def test_attribute_fails(self):
        """ Ensure that query an attribute from an offline media fails.
        """
        media_obj = _image_media.ImageMedia("/path/to/an/image.png")
        with self.assertRaises(media.MediaException):
            media_obj._set_media_information()

    def test_attribute_cached(self):
        """ Ensure media information is cached once gathered.
        """
        media_obj = _image_media.ImageMedia("/path/to/an/image.png")

        # Insert fake data to work around the information gathering.
        media_obj._info = {"width": "1920", "height": "1080"}  # pylint: disable=W0212

        self.assertEqual(resolution.Resolution(1920, 1080), media_obj.resolution)


class TestFrameRange(unittest.TestCase):
    """ Test ImageMedia frameRange computation.
    """

    def test_frameRange_default(self):
        """ Ensure an ImageMedia object defines a default (1, 1) frameRange.
        """
        media_obj = _image_media.ImageMedia("/path/to/an/image.png")
        frame_range = lite_media_core.path_utils.sequence.FrameRange(1, 1)

        self.assertEqual(frame_range, media_obj.frame_range)

    def test_frameRange_fromPath(self):
        """ Ensure an ImageMedia object defines a frameRange from path.
        """
        media_obj = _image_media.ImageMedia("/path/to/an/image.0125.png")
        frame_range = lite_media_core.path_utils.sequence.FrameRange(125, 125, padding=4)

        self.assertEqual(frame_range, media_obj.frame_range)
