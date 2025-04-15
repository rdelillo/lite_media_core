""" Test lite_media_core.media._media module.
"""
import os
import unittest

from lite_media_core import media


class TestMedia(unittest.TestCase):
    """ Ensure lite_media_core.media._media.Media base class implements correct features.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(TestMedia, self).setUp()

        imgPath = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "media",
            "img.dpx",
        )

        self.offlineMedia = media.Media("/path/to/offline/img.dpx")
        self.onlineMedia = media.Media(imgPath)

    def test_representAsStringOffline(self):
        """ Ensure a Media object represents correctly as string (offline).
        """
        self.assertEqual(
            "<Media '/path/to/offline/img.dpx' (image/x-dpx) offline>",
            str(self.offlineMedia),
        )

    def test_representAsStringOnline(self):
        """ Ensure a Media object represents correctly as string (online).
        """
        self.assertTrue("online" in str(self.onlineMedia))

    def test_represent(self):
        """ Ensure an offline Media object represents correctly.
        """
        self.assertEqual(
            "<Media path='/path/to/offline/img.dpx' (mimeType='image/x-dpx')>",
            repr(self.offlineMedia),
        )

    def test_iter(self):
        """ Ensure a Media can be iterated over itself.
        """
        result = [item for item in self.onlineMedia]
        self.assertEqual([self.onlineMedia], result)

    def test_eq_same(self):
        """ Ensure two identical media object are perceived as the same.
        """
        self.assertTrue(media.Media("/path/to/file/a") == media.Media("/path/to/file/a"))

    def test_eq_different(self):
        """ Ensure two different media object are not perceived as equal.
        """
        self.assertFalse(media.Media("/path/to/file/a") == media.Media("/path/to/file/b"))

    def test_eq_invalid(self):
        """ Ensure a TypeError is raised when checking if a media object is equal to a non media object.
        """
        with self.assertRaises(TypeError) as error:
            self.onlineMedia == "/path/to/file/a"  # pylint: disable=pointless-statement

        self.assertEqual(str(error.exception), "Invalid comparison between 'Media' and 'str'.")

    def test_ne_same(self):
        """ Ensure two identical media object are perceived as not equal.
        """
        self.assertFalse(media.Media("/path/to/file/a") != media.Media("/path/to/file/a"))

    def test_ne_different(self):
        """ Ensure two diffrent media object are not perceived as not equal.
        """
        self.assertTrue(media.Media("/path/to/file/a") != media.Media("/path/to/file/b"))

    def test_ne_invalid(self):
        """ Ensure a TypeError is raised when checking if a media object is not equal to a non media object.
        """
        with self.assertRaises(TypeError) as error:
            self.onlineMedia != "/path/to/file/a"  # pylint: disable=pointless-statement

        self.assertEqual(str(error.exception), "Invalid comparison between 'Media' and 'str'.")

    def test_hash(self):
        """ Ensure a Media object can be hashed.
        """
        inst1 = media.Media("/path/to/file/a")
        inst2 = media.Media(u"/path/to/file/a")
        inst3 = media.Media("/path/to/file/b")

        self.assertEqual({inst1, inst2, inst3}, {inst1, inst3})
        self.assertEqual(2, len({inst1, inst2, inst3}))

    def test_path(self):
        """ Ensure a Media object exposes a path.
        """
        self.assertEqual("/path/to/offline/img.dpx", self.offlineMedia.path)

    def test_type(self):
        """ Ensure a Media object exposes a type (mime-type).
        """
        self.assertEqual("image", self.offlineMedia.type)

    def test_subType(self):
        """ Ensure a Media object exposes a subType (mime-type).
        """
        self.assertEqual("x-dpx", self.offlineMedia.subType)

    def test_invalidMimeType(self):
        """ Ensure a Media object exposes conformed mime type.
        """
        mediaObj = media.Media("/path/to/offline/img.dpx", mimeType=5.0)  # invalid mime type
        self.assertEqual(
            (None, None),
            (mediaObj.type, mediaObj.subType),
        )

    def test_existsTrue(self):
        """ Ensure returns True for an online Media object.
        """
        self.assertTrue(self.onlineMedia.exists)

    def test_existsFalse(self):
        """ Ensure returns False for an offline Media object.
        """
        self.assertFalse(self.offlineMedia.exists)


class TestMediaFromPath(unittest.TestCase):
    """ Test that relevant Media objects can be created from path.
    """

    def test_unsupportedMimeType(self):
        """ Ensure a Media cannot be created from a path to an unsupported media.
        """
        self.assertRaises(
            media.UnsupportedMimeType,
            media.Media.fromPath,
            "/path/to/document/file.doc",  # not a media
        )

    def test_unknownMimeType(self):
        """ Ensure a Media cannot be created from an unknown file type.
        """
        self.assertRaises(
            media.UnsupportedMimeType,
            media.Media.fromPath,
            "/path/to/unknown/file.unknownExtension",  # unknown file mime-type
        )

    def test_audio(self):
        """ Ensure an Audio object is created from an audio file.
        """
        mediaObj = media.Media.fromPath("/path/to/an/audio/file.wav")
        self.assertIsInstance(mediaObj, media.Audio)

    def test_image(self):
        """ Ensure an Image object is created from an image file.
        """
        mediaObj = media.Media.fromPath("/path/to/an/image/file.png")
        self.assertIsInstance(mediaObj, media.Image)

    def test_imageSequence(self):
        """ Ensure an ImageSequence object is created from a sequence path.
        """
        mediaObj = media.Media.fromPath("/path/to/a/sequence/files.1001-1002#.png")
        self.assertIsInstance(mediaObj, media.ImageSequence)

    def test_image_vs_imageSequence(self):
        """ Ensure a frame padded single image is still an Image object (not a sequence).
        """
        mediaObj = media.Media.fromPath("/path/to/a/sequence/files.1001.png")
        self.assertIsInstance(mediaObj, media.ImageSequence)

    def test_video(self):
        """ Ensure a Movie object is created from a video file.
        """
        mediaObj = media.Media.fromPath("/path/to/a/video/file.mov")
        self.assertIsInstance(mediaObj, media.Movie)

    def test_video_alternativePath(self):
        """ Ensure a Movie object is created from a video file.
        """
        # Shall this later be a MovieSequence ?
        mediaObj = media.Media.fromPath("/path/to/a/video/file_0000-1001#.mov")
        self.assertIsInstance(mediaObj, media.Movie)

    def test_mxf(self):
        """ Ensure a Movie is created from an MXF file.
        """
        mediaObj = media.Media.fromPath("/path/to/a/mxf/file.mxf")
        self.assertIsInstance(mediaObj, media.Movie)
