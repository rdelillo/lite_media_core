""" Test lite_media_core._mediaInfo module.
"""
import tempfile
import unittest

from lite_media_core import _mediaInfo


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
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dpx") as tmpFile:
            # tempFile exists but is empty.
            self.assertRaises(
                ValueError,
                _mediaInfo.getMediaInformation,
                tmpFile.name,
            )
