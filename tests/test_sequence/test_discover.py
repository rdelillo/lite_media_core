""" Test cases for lite_media_core.path_utils.Sequence discovery
"""

# pylint: disable=too-many-public-methods

from __future__ import absolute_import

import inspect
import os
import shutil
import tempfile
import unittest

from lite_media_core.path_utils.sequence import Sequence


class TestSequenceDiscovery(unittest.TestCase):
    """ Ensure a lite_media_core.path_utils.Sequence can created from various incomplete string format.
    """

    def setUp(self):
        """ Set up
        """
        super(TestSequenceDiscovery, self).setUp()

        # Create two sequence
        # sequenceA have a padding of 3
        # sequenceB have a padding of 4
        # These two sequence are necessary to properly test
        # RV paths (which change depending on the padding)
        self._tmpDir = tempfile.mkdtemp()

        for relPath in (
            # leading zero, 3 padding
            "sequence/a.001.ext",
            "sequence/a.002.ext",
            "sequence/a.003.ext",
            "sequence/a.005.ext",
            "sequence/a.010.ext",
            # leading zero, 4 padding
            "sequence/b.0001.ext",
            "sequence/b.0002.ext",
            "sequence/b.0003.ext",
            "sequence/b.0005.ext",
            "sequence/b.0010.ext",
            # not leading zero
            "sequence/c.1.ext",
            "sequence/c.2.ext",
            "sequence/c.3.ext",
            "sequence/c.5.ext",
            "sequence/c.10.ext",
            # single frame
            "sequence/d.1001.ext",
            # not a sequence,
            "sequence/single_file.ext",
        ):
            path = os.path.join(self._tmpDir, relPath)
            directory = os.path.dirname(path)

            # Create directory
            if not os.path.isdir(directory):
                os.makedirs(directory)

            # Create file
            with open(path, "a"):
                os.utime(path, None)

        self.sequenceA = Sequence.fromString(os.path.join(self._tmpDir, "sequence/a.%03d.ext [1-3, 5, 10]"))
        self.sequenceB = Sequence.fromString(os.path.join(self._tmpDir, "sequence/b.%04d.ext [1-3, 5, 10]"))
        self.sequenceC = Sequence.fromString(os.path.join(self._tmpDir, "sequence/c.%d.ext [1-3, 5, 10]"))
        self.sequenceD = Sequence.fromString(os.path.join(self._tmpDir, "sequence/d.%d.ext 1001-1001"))

    def tearDown(self):
        """ Tear down
        """
        super(TestSequenceDiscovery, self).tearDown()

        if os.path.isdir(self._tmpDir):
            shutil.rmtree(self._tmpDir)

    def test_generator(self):
        """ Ensure discoverFromDisk return a generator.
        """
        value = os.path.join(self._tmpDir, "sequence/a.%03d.ext")
        result = Sequence.discoverFromDisk(value)
        self.assertTrue(inspect.isgenerator(result))

    def test_from_invalid_path(self):
        """ Ensure discoverFromDisk can't find a sequence from a path in a directory that don't exist.
        """
        value = os.path.join(self._tmpDir, "invalid_sequence", "%04d.png")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_from_sprintf(self):
        """ Ensure discoverFromDisk can find a sequence from a sprintf abstract path with correct padding.
        """
        value = os.path.join(self._tmpDir, "sequence/a.%03d.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceA})

    def test_from_sprintf_no_leading_zeroes(self):
        """ Ensure discoverFromDisk can find a sequence from a sprintf abstract path with non-zero padding.
                """
        value = os.path.join(self._tmpDir, "sequence/c.%d.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceC})

    def test_from_sprintf_wrong_padding(self):
        """ Ensure discoverFromDisk can't find a sequence from a sprintf abstract path with in-corect padding.
        """
        value = os.path.join(self._tmpDir, "sequence/a.%02d.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_from_houdini(self):
        """ Ensure discoverFromDisk can find a sequence from a houdini abstract path with correct padding.
        """
        value = os.path.join(self._tmpDir, "sequence/c.$F.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceC})

    def test_from_houdini_extended_with_padding(self):
        """ Ensure discoverFromDisk can find a sequence from
        a houdini extended abstract path with correct padding.
        """
        value = os.path.join(self._tmpDir, "sequence/a.$F3.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceA})

    def test_from_houdini_extended_with_wrong_padding(self):
        """ Ensure discoverFromDisk can't find a sequence from
        a houdini extended path with an incorrect padding.
        """
        value = os.path.join(self._tmpDir, "sequence/a.$F2.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_from_rv_dash(self):
        """ Ensure discoverFromDisk can find a sequence from a rv path using `#` with a correct padding.
        Note: SequenceB have a padding of 4 which should match `#`.
        """
        value = os.path.join(self._tmpDir, "sequence/b.#.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceB})

    def test_from_rv_dash_singleFrame(self):
        """ Ensure discoverFromDisk can find a sequence from a rv path using `#` with a correct padding.
        Note: SequenceB have a padding of 4 which should match `#`.  SHOULD IT THO???
        """
        value = os.path.join(self._tmpDir, os.path.join("sequence", "d.@@@@.ext"))
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceD})

    def test_ambiguous_leading_zeros(self):
        """ Ensure we discovering sequence with ambiguous leading zero, we consider no leading zeros.
        """
        value = os.path.join(self._tmpDir,os.path.join("sequence", "d.@@@@.ext"))
        sequence = tuple(Sequence.discoverFromDisk(value))[0]
        self.assertFalse(sequence.hasLeadingZeros)

    def test_from_rv_dash_wrong(self):
        """ Ensure discoverFromDisk can't find a sequence from a rv path using '#' with incorrect padding.
        Note: SequenceA have a padding of 3 which should not match '#'.
        """
        value = os.path.join(self._tmpDir, "sequence/a.#.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_from_rv_at(self):
        """ Ensure discoverFromDisk can find a sequence from a rv path using `@` with correct padding.
        """
        value = os.path.join(self._tmpDir, "sequence/a.@@@.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceA})

    def test_from_rv_no_leading_zeros(self):
        """ Ensure discoverFromDisk can find a sequence from a rv path using `@` with a non-zero padding.
        """
        value = os.path.join(self._tmpDir, "sequence/c.@@.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceC})

    def test_from_rv_at_wrong(self):
        """ Ensure discoverFromDisk can't find a sequence from a rv path using `@` with incorrect padding.
        """
        value = os.path.join(self._tmpDir, "sequence/a.@@.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_from_legacy_player(self):
        """ Ensure discoverFromDisk can find a sequence from a nuke path with correct padding.
        """
        value = os.path.join(self._tmpDir, "sequence/a.###.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceA})

    def test_from_legacy_player_no_leading_zeros(self):
        """ Ensure discoverFromDisk can find a sequence from a legacy path with non-zero padding.
        """
        value = os.path.join(self._tmpDir, "sequence/c.##.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceC})

    def test_from_legacy_player_wrong(self):
        """ Ensure discoverFromDisk can find a sequence from a nuke path with correct padding.
        """
        value = os.path.join(self._tmpDir, "sequence/a.#####.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_from_unix_wildcard_wrong(self):
        """ Ensure discoverFromDisk can't find a sequence from path with unix path that don't match any file.
        """
        value = os.path.join(self._tmpDir, "sequence/a.wrong.*.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_from_unix_wildcard(self):
        """ Ensure discoverFromDisk can find a sequence from a path with unix pattern in the file name part.
        """
        value = os.path.join(self._tmpDir, "sequence/a.*.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceA})

    def test_from_unix_wildcard_nested_and_nuke(self):
        """ Ensure discoveryFromDisk can find a sequence from a combination of unix and nuke patterns.
        """
        value = os.path.join(self._tmpDir, "*/*.%03d.ext")  # should only match sequenceA
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceA})

    def test_from_unit_wildcard_and_nuke_wrong(self):
        """ Ensure discoveryFromDisk can't find a sequence from a combination of unix and nuke patterns.
        """
        value = os.path.join(self._tmpDir, "*/*.%05d.ext")  # should only match sequenceA
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_from_unix_wildcard_directory_and_nuke_extended(self):
        """ Ensure discoverFromDisk can find a sequence from a unix pattern in the directory part.
        """
        value = os.path.join(self._tmpDir, "*/a.%03d.ext 1-10")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceA})

    def test_from_unix_wildcard_nested(self):
        """ Ensure discoverFromDisk can find a sequence from
        a unix nested abstract path that match some files.
        """
        value = os.path.join(self._tmpDir, "*/*.ext")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, {self.sequenceA, self.sequenceB, self.sequenceC, self.sequenceD})

    def test_from_unix_wildcard_nested_wrong(self):
        """ Ensure discoverFromDisk can find a sequence from
        a unix nested abstract path that match some files.
        """
        value = os.path.join(self._tmpDir, "*/*.BAD_EXTENSION")
        result = set(Sequence.discoverFromDisk(value))
        self.assertEqual(result, set())

    def test_iter_sequence_directory(self):
        """ Ensure getSequences can find sequences from a directory path.
        """
        result = set(Sequence.getSequences(os.path.join(self._tmpDir, "sequence")))
        self.assertEqual(result, {self.sequenceA, self.sequenceB, self.sequenceC, self.sequenceD})
