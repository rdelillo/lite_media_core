""" Test lite_media_core.media._imageMedia module.
"""
import os
import tempfile
import platform
import unittest

import mock

import lite_media_core.path_utils

from lite_media_core import media
from lite_media_core.media import _imageMedia
from lite_media_core import resolution

mediaPath = _mediaPath = os.path.join(
    os.path.dirname(__file__),
    "..",
    "resources",
    "media",
)


class TestImageMedia(unittest.TestCase):
    """ Test the generic ImageMedia class (raw, image, movie...).
    """
    def setUp(self):
        """ Set up the testing class.
        """
        super(TestImageMedia, self).setUp()

        imgMediaPath = os.path.join(mediaPath, "img.png")
        self.imgMedia = _imageMedia.ImageMedia(imgMediaPath)  # test with an image file

    def test_resolution(self):
        """ Ensure the resolution parameter is properly read from an ImageMedia object.
        """
        expected = resolution.Resolution(64, 64)
        self.assertEqual(expected, self.imgMedia.resolution)

    def test_resolutionAnamorphic(self):
        """ Ensure an anamorphic resolution is properly read from an ImageMedia object.
        """
        expected = resolution.Resolution(64, 64, pixelAspectRatio=2.0)
        anaImgMediaPath = os.path.join(mediaPath, "img-anamorphic.exr")
        imgMedia = _imageMedia.ImageMedia(anaImgMediaPath)

        self.assertEqual(expected, imgMedia.resolution)

    def test_metadata(self):
        """ Ensure the metadata can be retrieved from an ImageMedia object.
        """
        self.assertTrue(self.imgMedia.metadata)

    def test_delayLoad(self):
        """ Ensure media information gathering is delayed for an ImageMedia.
        """
        mediaObj = _imageMedia.ImageMedia("/path/to/an/image.png")
        self.assertEqual(
            (None, None),
            (mediaObj._info, mediaObj._metadata),  # pylint: disable=W0212
        )

    def test_init_fails(self):
        """ Ensure an ImageMedia object cannot be created from an unsupported format.
        """
        self.assertRaises(
            media.UnsupportedMimeType,
            _imageMedia.ImageMedia,
            "/path/to/an/audio.wav",
        )

    def test_attribute_fails(self):
        """ Ensure that query an attribute from an offline media fails.
        """
        mediaObj = _imageMedia.ImageMedia("/path/to/an/image.png")
        self.assertRaises(
            media.MediaException,
            mediaObj._setMediaInformation,  # pylint: disable=W0212
        )

    def test_attribute_cached(self):
        """ Ensure media information is cached once gathered.
        """
        mediaObj = _imageMedia.ImageMedia("/path/to/an/image.png")

        # Insert fake data to work around the information gathering.
        mediaObj._info = {"width": "1920", "height": "1080"}  # pylint: disable=W0212

        self.assertEqual(resolution.Resolution(1920, 1080), mediaObj.resolution)


class TestFrameRange(unittest.TestCase):
    """ Test ImageMedia frameRange computation.
    """

    def test_frameRange_default(self):
        """ Ensure an ImageMedia object defines a default (1, 1) frameRange.
        """
        mediaObj = _imageMedia.ImageMedia("/path/to/an/image.png")
        frameRange = lite_media_core.path_utils.sequence.FrameRange(1, 1)

        self.assertEqual(frameRange, mediaObj.frameRange)

    def test_frameRange_fromPath(self):
        """ Ensure an ImageMedia object defines a frameRange from path.
        """
        mediaObj = _imageMedia.ImageMedia("/path/to/an/image.0125.png")
        frameRange = lite_media_core.path_utils.sequence.FrameRange(125, 125, padding=4)

        self.assertEqual(frameRange, mediaObj.frameRange)
