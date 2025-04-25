""" Test lite_media_core._mediaInfo module.
"""
import tempfile
import unittest

from lite_media_core import _media_info


class TestMediaInfo(unittest.TestCase):
    """ Test lite_media_core._mediaInfo init.
    """
    def test_wrongFile_fails(self):
        """ Ensure trying to get information from a file which does not exist fails.
        """
        with self.assertRaises(ValueError):
            _ = _media_info.get_media_information("/path/to/not/existing/file.ext")

    def test_unsupportedFile_fails(self):
        """ Ensure trying to get information from an unsupported file fails.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dpx") as tmpFile:
            # tempFile exists but is empty.
            with self.assertRaises(ValueError):
                _ =  _media_info.get_media_information(tmpFile.name)
