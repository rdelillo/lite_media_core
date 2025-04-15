""" Test cases for the lite_media_core.path_utils.path module
"""
from __future__ import absolute_import

import unittest
import mock

import lite_media_core.path_utils.path


class TestSplitext(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.path.splitext function.
    """

    def test_splitext_known(self):
        """ Ensure splitext can return the correct (root, ext) for a known type.
        """
        self.assertEqual(
            ("/path/to/an/image", ".dpx"), lite_media_core.path_utils.path.splitext("/path/to/an/image.dpx"),
        )

    def test_splitext_unknown(self):
        """ Ensure splitext default to os.path.splitext for an unknown type.
        """
        self.assertEqual(
            ("/path/to/a/file", ".ext"), lite_media_core.path_utils.path.splitext("/path/to/a/file.ext"),
        )

    def test_splitext_raise(self):
        """ Ensure splitext default to os.path.splitext raises when the provided type is unknown.
        """
        path = "file.definitely_not_a_valid_extension"
        with self.assertRaises(ValueError):
            _ = lite_media_core.path_utils.path.splitext(path, allowUnknownType=False)
