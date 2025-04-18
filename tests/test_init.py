""" Test out lite_media_core.path_utils.__init__ module.
"""
import unittest

import lite_media_core.path_utils


class TestGetSequences(unittest.TestCase):
    """ Test out lite_media_core.path_utils.getSequences feature.
    """

    def test_getSequences_empty(self):
        """ Ensure an empty list is returned when no singleFile or Sequence file could be found.
        """
        self.assertEqual([], list(lite_media_core.path_utils.getSequences([])))

    def test_unambiguous_leadingZeros_positive(self):
        """Ensure getSequences return a zero padded sequence if zero padding is hinted.
        """
        for data in (
            ["img.01.ext", "img.02.ext"],
            ["img.%04d.exr 1-10"],
        ):
            self.assertTrue(next(lite_media_core.path_utils.getSequences(data)).hasLeadingZeros, msg=data)

    def test_unambiguous_leadingZeros_negative(self):
        """Ensure getSequences return a non-zero padded sequence if non-zero padding is hinted.
        """
        for data in (
            ["img.1.ext", "img.2.ext"],
            ["img.%d.exr 1-10"],
        ):
            self.assertFalse(next(lite_media_core.path_utils.getSequences(data)).hasLeadingZeros, msg=data)

    def test_ambiguous_leadingZeros_defaultFalse(self):
        """Ensure getSequences return a non-zero padded sequence if zero padding is ambiguous.
        """
        self.assertFalse(next(lite_media_core.path_utils.getSequences(["img.10.exr", "img.11.exr"])).hasLeadingZeros)
