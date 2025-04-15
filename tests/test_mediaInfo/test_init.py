""" Test lite_media_core._mediaInfo module.
"""
import os
import tempfile
import unittest

from lite_media_core import _mediaInfo


@unittest.skip("Setup identifier properly")
class TestMediaInfo(unittest.TestCase):
    """ Test lite_media_core._mediaInfo init.
    """
    def test_wrongFile_fails(self):
        """ Ensure trying to get information from a file which does not exist fails.
        """
        self.assertRaises(
            ValueError,
            _mediaInfo.getMediaInformation,
            "/path/to/not/existing/file.ext",
        )

    def test_unsupportedFile_fails(self):
        """ Ensure trying to get information from an unsupported file fails.
        """
        tmpFile = tempfile.NamedTemporaryFile(delete=False, suffix=".dpx")  # temporary file
        tmpFile.close()

        self.assertRaises(
            ValueError,
            _mediaInfo.getMediaInformation,
            tmpFile.name,
        )

    def test_getInformation(self):
        """ Ensure getMediaInfo returns data from a proper media file.
        """
        mediaPath = os.path.join(
            os.path.dirname(__file__),
            "..",
            "resources",
            "media",
        )
        path = os.path.join(mediaPath, "img.png")
        information = {
            "bits": "8",
            "channels": "3",
            "height": "64",
            "pixelAspectRatio": "1",
            "width": "64"

        }
        metadata = {"PNG/ColorType": "RGB"}

        self.assertEqual(
            (information, metadata),
            _mediaInfo.getMediaInformation(path),
        )
