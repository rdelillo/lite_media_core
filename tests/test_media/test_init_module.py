""" Test lite_media_core.media module.
"""
import inspect
import unittest

from lite_media_core import media


class TestMediaInit(unittest.TestCase):
    """ Ensure the __init__ module of lite_media_core.media exposes correct classes.
    """
    def test_Audio(self):
        """ Ensure lite_media_core.media exposes Audio.
        """
        audioClass = media.Audio
        self.assertTrue(inspect.isclass(audioClass))

    def test_Image(self):
        """ Ensure lite_media_core.media exposes Image.
        """
        imageClass = media.Image
        self.assertTrue(inspect.isclass(imageClass))

    def test_ImageSequence(self):
        """ Ensure lite_media_core.media exposes ImageSequence.
        """
        imageSequenceClass = media.ImageSequence
        self.assertTrue(inspect.isclass(imageSequenceClass))

    def test_Media(self):
        """ Ensure lite_media_core.media exposes Media.
        """
        mediaClass = media.Media
        self.assertTrue(inspect.isclass(mediaClass))

    def test_MediaException(self):
        """ Ensure lite_media_core.media exposes MediaException.
        """
        mediaExceptionClass = media.MediaException
        self.assertTrue(inspect.isclass(mediaExceptionClass))

    def test_Movie(self):
        """ Ensure lite_media_core.media exposes Movie.
        """
        movieClass = media.Movie
        self.assertTrue(inspect.isclass(movieClass))

    def test_UnsupportedMimeType(self):
        """ Ensure lite_media_core.media exposes UnsupportedMimeType.
        """
        unsupportedMimeTypeClass = media.UnsupportedMimeType
        self.assertTrue(inspect.isclass(unsupportedMimeTypeClass))
