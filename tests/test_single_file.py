""" Test out the lite_media_core.path_utils.singleFile module.
"""
import unittest
import os

from lite_media_core.path_utils import single_file
from lite_media_core.path_utils import sequence


class TestSingleFile(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.single_file.SingleFile object.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(TestSingleFile, self).setUp()
        self.single_file = single_file.SingleFile("/path/to/a/file.ext")

    def test_representation(self):
        """ Ensure a SingleFile object represents itself correctly.
        """
        self.assertEqual("<SingleFile /path/to/a/file.ext>", repr(self.single_file))

    def test_representationAsString(self):
        """ Ensure a SingleFile object represents itself correctly as string.
        """
        self.assertEqual("/path/to/a/file.ext", str(self.single_file))

    def test_hash(self):
        """ Ensure a SingleFile object defines a hash.
        """
        same = single_file.SingleFile("/path/to/a/file.ext")
        self.assertEqual(hash(same), hash(self.single_file))

    def test_equal(self):
        """ Compare a SingleFile with another single_file.
        """
        same = single_file.SingleFile("/path/to/a/file.ext")
        different = single_file.SingleFile("/path/to/another/file.ext")

        self.assertTrue(self.single_file == same)
        self.assertTrue(self.single_file != different)

    def test_equal_sequence(self):
        """ Compare a SingleFile with a Sequence.
        """
        sFile = single_file.SingleFile(os.path.join(os.sep, "file.01.ext"))
        same = sequence.Sequence.from_string(os.path.join(os.sep, "file.01.ext"))
        different = sequence.Sequence.from_string("another_file.01-02#.ext")

        self.assertTrue(sFile == same)
        self.assertTrue(sFile != different)

    def test_iter(self):
        """ Ensure we can iterate over a single_file.
        """
        self.assertEqual(["/path/to/a/file.ext"], list(self.single_file))
