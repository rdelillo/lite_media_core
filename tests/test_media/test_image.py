""" Test lite_media_core.media._image module.
"""
# pylint: disable=too-many-public-methods
import os
import shutil
import tempfile
import unittest

import lite_media_core.path_utils

from lite_media_core import media
from lite_media_core.media import _image

mediaPath = _mediaPath = os.path.join(
    os.path.dirname(__file__),
    "..",
    "resources",
    "media",
)


class TestImage(unittest.TestCase):
    """ Test lite_media_core.media.Image class.
    """
    def test_failsNotFromImage(self):
        """ Ensure an Image object fails when not created from an image file.
        """
        self.assertRaises(
            media.UnsupportedMimeType,
            media.Image,
            "/path/to/a/video.mov",
        )


class TestImageSequence(unittest.TestCase):
    """ Test lite_media_core.media.Image class.
    """
    def setUp(self):
        """ Set up testing class.
        """
        super(TestImageSequence, self).setUp()

        # Prepare a temporary image sequence.
        self.tempdir = tempfile.gettempdir()
        self.imgSequence = media.ImageSequence(os.path.join(self.tempdir, "img.1001-1003#.png"))

    def test_initializeFromSequence(self):
        """ Validate we can initialize an ImageSequence from a sequence object and that the
        ImageSequence reflect the original Sequence.
        """
        sequence = lite_media_core.path_utils.sequence.Sequence.fromString(
            os.path.join(self.tempdir, "img.1001-1003#.png")
        )
        inst = media.ImageSequence(sequence)

        for attr in ('start', 'end', 'head', 'tail'):
            self.assertEqual(
                getattr(sequence, attr),
                getattr(inst, attr)
            )

    def test_initializeNotFromSequence_fails(self):
        """ Ensure cannot create an ImageSequence media from a none-sequence media path.
        """
        self.assertRaises(
            ValueError,
            media.ImageSequence,
            "/path/to/a/single/image.png",
        )

    def test_representAsStr(self):
        """ Ensure an ImageSequence object represents as string correctly.
        """
        self.assertEqual(
            "<ImageSequence %r (image/png) offline>" % os.path.join(self.tempdir, "img.1001-1003#.png"),
            str(self.imgSequence)
        )

    def test_represent(self):
        """ Ensure an ImageSequence object represents correctly.
        """
        self.assertEqual(
            "<ImageSequence path='%s' (mimeType='image/png')>" % os.path.join(self.tempdir, "img.1001-1003#.png"),
            repr(self.imgSequence)
        )

    def test_path(self):
        """ Ensure the path from an ImageSequence is consistent.
        """
        self.assertEqual(
            os.path.join(self.tempdir, "img.1001-1003#.png"),
            self.imgSequence.path
        )

    def test_frameRange(self):
        """ Ensure the frame range can be retrieved from an ImageSequence.
        """
        frameRange = lite_media_core.path_utils.sequence.FrameRange(1001, 1003)
        self.assertEqual(frameRange, self.imgSequence.frameRange)

    def test_invalidFrameRange(self):
        """ Ensure trying to access a frame range from an none-existing ImageSequence.
        """
        with self.assertRaises(ValueError):
            _ = media.ImageSequence("/path/to/frame/sequence.#.png")

    def test_isValid(self):
        """ Ensure a sequence can be validated. More test in utils testing class.
        """
        self.assertTrue(self.imgSequence.validate())

    def test_attributesLinkToFirstFrame(self):
        """ Ensure that the basic media attributes link to the first frame.
        """
        # Copy required image so they are online.
        for idx in range(1001, 1003):
            shutil.copy(
                os.path.join(mediaPath, "img.png"),
                os.path.join(self.tempdir, "img.%d.png" % idx),
            )

        firstFrameMedia = _image.Image(os.path.join(self.tempdir, "img.1001.png"))
        imgSequence = media.ImageSequence(os.path.join(self.tempdir, "img.1001-1002#.png"))

        try:
            self.assertEqual(
                (firstFrameMedia.resolution, firstFrameMedia.metadata, firstFrameMedia.subType),
                (imgSequence.resolution, imgSequence.metadata, imgSequence.subType),
            )

        finally:
            # Clean up copied images.
            for idx in range(1001, 1003):
                os.remove(os.path.join(self.tempdir, "img.%d.png" % idx))

    def test_iter(self):
        """ Ensure an ImageSequence object is iterable.
        """
        expected = [
            os.path.join(self.tempdir, "img.1001.png"),
            os.path.join(self.tempdir, "img.1002.png"),
            os.path.join(self.tempdir, "img.1003.png"),
        ]
        result = [image.path for image in self.imgSequence]

        self.assertEqual(expected, result)

    def test_missing_image(self):
        """ Ensure explicit missing frames from an image sequence are properly handled.
        """
        imageSequence = media.ImageSequence("sequence.%04d.exr 1-10 ([2,4,6,8])")

        self.assertEqual(
            (
                6,
                True,
            ),
            (
                len(imageSequence),
                all([isinstance(miss, media.Image) for miss in imageSequence.missing]),
            ),
        )

    def test_getitem(self):
        """ Ensure images can be accessed from a sequence through indexes.
        """
        self.assertEqual(
            (os.path.join(self.tempdir, "img.1001.png"), os.path.join(self.tempdir, "img.1003.png")),
            (self.imgSequence[0].path, self.imgSequence[-1].path),
        )

    def test_len(self):
        """ Ensure ImageSequence length corresponds to images.
        """
        seqMedia = media.ImageSequence("img.2-102#.png")
        frameRange = lite_media_core.path_utils.sequence.FrameRange(2, 102, padding=3)

        self.assertEqual(
            (frameRange, 101),
            (seqMedia.frameRange, len(seqMedia)),
        )

    def test_imageSequence_fromImages(self):
        """ Ensure an image sequence can be created from image paths.
        """
        seqMedia = media.ImageSequence("img.1001-1003#.png")
        imgMedia = seqMedia[0]

        self.assertIsInstance(imgMedia, media.Image)

    def test_imageSequence_invalidImages_fails(self):
        """ Ensure an image sequence cannot be created with files other than image.
        """
        self.assertRaises(
            ValueError,
            media.ImageSequence,
            "video.1-3#.mov",
        )

    def test_imageSequence_properties(self):
        """ Ensure 'sequence' based properties can be retrieved from an ImageSequence.
        """
        self.assertEqual(
            (
                'img.',
                '.png',
                4,
                [],
            ),
            (
                self.imgSequence.head,
                self.imgSequence.tail,
                self.imgSequence.padding,
                self.imgSequence.missing,
            ),
        )

    def test_imageSequence_attributeError(self):
        """ Ensure despite redirecting its attribute to the sequence object, invalid attributes still raise.
        """
        with self.assertRaises(AttributeError):
            _ = self.imgSequence.wrongAttribute

    def test_imageSequence_fromList(self):
        """ Ensure an ImageSequence object can be created from a list of file paths.
        """
        mediaObj = _image.ImageSequence.fromList(
            [
                "/path/to/file.0000.exr",
                "/path/to/file.0005.exr",
                "/path/to/file.0006.exr",
                "/path/to/file.0007.exr",
            ]
        )

        self.assertEqual(
            (
                True,
                0, 
                7,
                [1, 2, 3, 4],
            ),
            (
                isinstance(mediaObj, _image.ImageSequence),
                mediaObj.frameRange.start,
                mediaObj.frameRange.end,
                list(img.frameRange.start for img in mediaObj.missing),
            )
        )

    def test_imageSequence_fromList_singleEntry(self):
        """ Ensure an Image object can be created from a list of 1 file paths.
        """
        mediaObj = _image.ImageSequence.fromList(["file.0000.exr"])

        self.assertEqual(
            (
                True,
                os.path.join(os.getcwd(), "file.0000.exr"),
            ),
            (
                isinstance(mediaObj, _image.ImageSequence),
                mediaObj.path,
            )
        )


class TestImageSequenceUtils(unittest.TestCase):
    """ Test lite_media_core.media._image utilities.
    """
    def test_validateSequence(self):
        """ Test with a valid media sequence.
        """
        imageMedias = [
            media.Image("/path/to/an/image1.png"),
            media.Image("/path/to/an/image2.png"),
        ]

        self.assertTrue(_image._validateSequence(imageMedias))  # pylint: disable=W0212

    def test_validateSequence_invalidEmpty(self):
        """ Test invalid sequence (empty).
        """
        self.assertRaises(ValueError, _image._validateSequence, [])  # pylint: disable=W0212

    def test_validateSequence_invalidMixTypes(self):
        """ Test invalid sequence (mix of mime types).
        """
        imageMedias = [
            media.Image(os.path.join(mediaPath, "img.dpx")),
            media.Image(os.path.join(mediaPath, "img.png")),
        ]

        self.assertRaises(
            ValueError,
            _image._validateSequence,  # pylint: disable=W0212
            imageMedias,
        )

    def test_validateSequence_invalidMissingFrame(self):
        """ Test invalid sequence (mix or existing and missing).
        """
        imageMedias = [
            media.Image(os.path.join(mediaPath, "img.dpx")),
            media.Image("/path/to/a/missing/image.dpx"),
        ]

        self.assertRaises(
            ValueError,
            _image._validateSequence,  # pylint: disable=W0212
            imageMedias,
        )

    def test_validateSequence_invalidInconsistentResolution(self):
        """ Test invalid sequence (inconsistent resolution).
        """
        imageMedias = [
            media.Movie(os.path.join(mediaPath, "video.mov")),  # 512x512
            media.Movie(os.path.join(mediaPath, "video_with_tc.mov")),  # 256x256
        ]

        self.assertRaises(
            ValueError,
            _image._validateSequence,  # pylint: disable=W0212
            imageMedias,
        )
