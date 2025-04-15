""" Test out the lite_media_core.path_utils.singleFile module.
"""
from __future__ import absolute_import

import unittest
import os

from lite_media_core.path_utils import singleFile
from lite_media_core.path_utils import sequence


class TestSingleFile(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.singleFile.SingleFile object.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(TestSingleFile, self).setUp()
        self.singleFile = singleFile.SingleFile("/path/to/a/file.ext")

    def test_representation(self):
        """ Ensure a SingleFile object represents itself correctly.
        """
        self.assertEqual("<SingleFile '/path/to/a/file.ext'>", repr(self.singleFile))

    def test_representationAsString(self):
        """ Ensure a SingleFile object represents itself correctly as string.
        """
        self.assertEqual("/path/to/a/file.ext", str(self.singleFile))

    def test_hash(self):
        """ Ensure a SingleFile object defines a hash.
        """
        same = singleFile.SingleFile("/path/to/a/file.ext")
        self.assertEqual(hash(same), hash(self.singleFile))

    def test_equal(self):
        """ Compare a SingleFile with another SingleFile.
        """
        same = singleFile.SingleFile("/path/to/a/file.ext")
        different = singleFile.SingleFile("/path/to/another/file.ext")

        self.assertTrue(self.singleFile == same)
        self.assertTrue(self.singleFile != different)

    def test_equal_sequence(self):
        """ Compare a SingleFile with a Sequence.
        """
        sFile = singleFile.SingleFile(os.path.join(os.sep, "file.01.ext"))
        same = sequence.Sequence.fromString(os.path.join(os.sep, "file.01.ext"))
        different = sequence.Sequence.fromString("another_file.01-02#.ext")

        self.assertTrue(sFile == same)
        self.assertTrue(sFile != different)

    def test_iter(self):
        """ Ensure we can iterate over a SingleFile.
        """
        self.assertEqual(["/path/to/a/file.ext"], list(self.singleFile))
