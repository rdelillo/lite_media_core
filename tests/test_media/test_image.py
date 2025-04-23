""" Test lite_media_core.media._image module.
"""
# pylint: disable=too-many-public-methods
import os
import shutil
import tempfile
import unittest

from lite_media_core import media
from lite_media_core import path_utils
from lite_media_core.media import _image

media_path = _mediaPath = os.path.join(
    os.path.dirname(__file__),
    "..",
    "resources",
    "media",
)


class TestImage(unittest.TestCase):
    """ Test lite_media_core.media.Image class.
    """
    def test_fails_not_from_Image(self):
        """ Ensure an Image object fails when not created from an image file.
        """
        with self.assertRaises(media.UnsupportedMimeType):
            _ = media.Image("/path/to/a/video.mov")


class TestImageSequence(unittest.TestCase):
    """ Test lite_media_core.media.Image class.
    """
    def setUp(self):
        """ Set up testing class.
        """
        super(TestImageSequence, self).setUp()

        # Prepare a temporary image sequence.
        self.tempdir = tempfile.gettempdir()
        self.img_sequence = media.ImageSequence(os.path.join(self.tempdir, "img.1001-1003#.png"))

    def test_initializeFromSequence(self):
        """ Validate we can initialize an ImageSequence from a sequence object and that the
        ImageSequence reflect the original Sequence.
        """
        sequence = path_utils.sequence.Sequence.from_string(
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
        with self.assertRaises(ValueError):
            _ = media.ImageSequence("/path/to/a/single/image.png")

    def test_representAsStr(self):
        """ Ensure an ImageSequence object represents as string correctly.
        """
        out_path = os.path.join(self.tempdir, "img.####.png 1001-1003")
        self.assertEqual(
            f"<ImageSequence '{out_path}' (image/png) offline>",
            str(self.img_sequence)
        )

    def test_represent(self):
        """ Ensure an ImageSequence object represents correctly.
        """
        self.assertEqual(
            "<ImageSequence path='%s' (mimeType='image/png')>" % os.path.join(self.tempdir, "img.####.png 1001-1003"),
            repr(self.img_sequence)
        )

    def test_path(self):
        """ Ensure the path from an ImageSequence is consistent.
        """
        self.assertEqual(
            os.path.join(self.tempdir, "img.####.png 1001-1003"),
            self.img_sequence.path
        )

    def test_frameRange(self):
        """ Ensure the frame range can be retrieved from an ImageSequence.
        """
        frame_range = path_utils.sequence.FrameRange(1001, 1003)
        self.assertEqual(frame_range, self.img_sequence.frame_range)

    def test_invalidFrameRange(self):
        """ Ensure trying to access a frame range from an none-existing ImageSequence.
        """
        with self.assertRaises(ValueError):
            _ = media.ImageSequence("/path/to/frame/sequence.#.png")

    def test_isValid(self):
        """ Ensure a sequence can be validated. More test in utils testing class.
        """
        self.assertTrue(self.img_sequence.validate())

    def test_attributesLinkToFirstFrame(self):
        """ Ensure that the basic media attributes link to the first frame.
        """
        # Copy required image so they are online.
        for idx in range(1001, 1003):
            shutil.copy(
                os.path.join(media_path, "img.png"),
                os.path.join(self.tempdir, "img.%d.png" % idx),
            )

        first_frame = _image.Image(os.path.join(self.tempdir, "img.1001.png"))
        img_sequence = media.ImageSequence(os.path.join(self.tempdir, "img.1001-1002#.png"))

        try:
            self.assertEqual(
                (first_frame.resolution, first_frame.metadata, first_frame.sub_type),
                (img_sequence.resolution, img_sequence.metadata, img_sequence.sub_type),
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
        result = [image.path for image in self.img_sequence]

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
            (self.img_sequence[0].path, self.img_sequence[-1].path),
        )

    def test_len(self):
        """ Ensure ImageSequence length corresponds to images.
        """
        seqMedia = media.ImageSequence("img.2-102#.png")
        frameRange = path_utils.sequence.FrameRange(2, 102, padding=3)

        self.assertEqual(
            (frameRange, 101),
            (seqMedia.frame_range, len(seqMedia)),
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
        with self.assertRaises(ValueError):
            _ = media.ImageSequence("video.1-3#.mov")

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
                self.img_sequence.head,
                self.img_sequence.tail,
                self.img_sequence.padding,
                self.img_sequence.missing,
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
        media_obj = _image.ImageSequence.from_list(
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
                isinstance(media_obj, _image.ImageSequence),
                media_obj.frame_range.start,
                media_obj.frame_range.end,
                list(img.frame_range.start for img in media_obj.missing),
            )
        )

    def test_imageSequence_fromList_singleEntry(self):
        """ Ensure an Image object can be created from a list of 1 file paths.
        """
        media_obj = _image.ImageSequence.from_list(["file.0000.exr"])

        self.assertEqual(
            (
                True,
                os.path.join(os.getcwd(), "file.0000.exr"),
            ),
            (
                isinstance(media_obj, _image.ImageSequence),
                media_obj.path,
            )
        )


class TestImageSequenceUtils(unittest.TestCase):
    """ Test lite_media_core.media._image utilities.
    """
    def test_validateSequence(self):
        """ Test with a valid media sequence.
        """
        image_media = [
            media.Image("/path/to/an/image1.png"),
            media.Image("/path/to/an/image2.png"),
        ]

        self.assertTrue(_image._validate_sequence(image_media))  # pylint: disable=W0212

    def test_validate_sequence_invalidEmpty(self):
        """ Test invalid sequence (empty).
        """
        with self.assertRaises(ValueError):
            _ = _image._validate_sequence([])  # pylint: disable=W0212

    def test_validate_sequence_invalidMixTypes(self):
        """ Test invalid sequence (mix of mime types).
        """
        image_media = [
            media.Image(os.path.join(media_path, "img.dpx")),
            media.Image(os.path.join(media_path, "img.png")),
        ]

        with self.assertRaises(ValueError):
            _ = _image._validate_sequence(image_media)  # pylint: disable=W0212

    def test_validate_sequence_invalidMissingFrame(self):
        """ Test invalid sequence (mix or existing and missing).
        """
        image_media = [
            media.Image(os.path.join(media_path, "img.dpx")),
            media.Image("/path/to/a/missing/image.dpx"),
        ]

        with self.assertRaises(ValueError):
            _ = _image._validate_sequence(image_media)  # pylint: disable=W0212

    def test_validate_sequence_invalidInconsistentResolution(self):
        """ Test invalid sequence (inconsistent resolution).
        """
        image_medias = [
            media.Movie(os.path.join(media_path, "video.mov")),  # 512x512
            media.Movie(os.path.join(media_path, "video_with_tc.mov")),  # 256x256
        ]

        with self.assertRaises(ValueError):
            _ = _image._validate_sequence(image_medias)  # pylint: disable=W0212
