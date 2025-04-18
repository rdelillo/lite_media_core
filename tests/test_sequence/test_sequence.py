""" Test out the lite_media_core.path_utils.sequence._sequence module.
"""
import os
import shutil
import tempfile
import unittest

import fileseq

from lite_media_core.path_utils import sequence


class TestSequenceAbsolute(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.sequence._sequence module from an absolute path.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(TestSequenceAbsolute, self).setUp()
        self._sequence_dirname = os.path.abspath(os.path.join(os.sep, "path", "to", "a"))
        self._sequence_basename = os.path.join(self._sequence_dirname, "file.")
        sequence_string = self._sequence_basename + "%04d.ext" + " " + "1001-1005"
        self._sequence = sequence.Sequence.fromString(sequence_string)

    def test_properties(self):
        """ Ensure the Sequence properties are valid.
        """
        self.assertEqual(
            (
                "file.",
                ".ext",
                self._sequence_basename + "1001.ext",
                self._sequence_basename + "1005.ext",
                [],
                4,
            ),
            (
                self._sequence.head,
                self._sequence.tail,
                self._sequence.start,
                self._sequence.end,
                self._sequence.missing,
                self._sequence.padding,
            ),
        )

    def test_paddedUniqueFile(self):
        """ Ensure a Sequence can be build from a padded file string.
        """
        first_frame = self._sequence_basename + "1001.ext"
        seq = sequence.Sequence.fromString(first_frame)
        self.assertTrue(first_frame== seq.start == seq.end)

    def test_paddedUniqueFile_r3d(self):
        """ Ensure a Sequence can be build from a padded file string.
        """
        unique_file = os.path.abspath(os.path.join("path", "to", "a", "file.") + "1001.cr2")
        seq = sequence.Sequence.fromString(unique_file)
        self.assertTrue(unique_file == seq.start == seq.end)

    def test_unpaddedUniqueFile(self):
        """ Ensure a Sequence cannot be build from an unpadded file string.
        """
        with self.assertRaises(ValueError):
            _ = sequence.Sequence.fromString("/path/to/an/unpadded/file.ext")

        with self.assertRaises(ValueError):
            _ = sequence.Sequence.fromString("/path/to/an/unpadded/file.ext2")

        with self.assertRaises(ValueError):
            _ = sequence.Sequence.fromString("/path/to/an/unpadded/file.R3D")

    def test_representation(self):
        """ Ensure a Sequence represents correctly.
        """
        self.assertEqual(
            "<Sequence <FileSequence: '"+ self._sequence_basename + "1001-1005#.ext'>>",
            repr(self._sequence),
        )

    def test_representationAsString(self):
        """ Ensure a Sequence represents correctly as string.
        """
        self.assertEqual(
            "<Sequence '" + self._sequence_basename + "####.ext 1001-1005'>",
            str(self._sequence),
        )

    def test_iter(self):
        """ Ensure the Sequence can be iterated over.
        """
        self.assertEqual(
            [
                self._sequence_basename + "1001.ext",
                self._sequence_basename + "1002.ext",
                self._sequence_basename + "1003.ext",
                self._sequence_basename + "1004.ext",
                self._sequence_basename + "1005.ext",
            ],
            list(self._sequence),
        )

    def test_equals(self):
        """ Ensure we can compare two similar sequences.
        """
        self.assertEqual(
            sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1005"),
            sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1005"),
        )

    def test_not_equals(self):
        """ Ensure we can compare two different sequences.
        """
        self.assertNotEqual(
            sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1005"),
            sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1004"),
        )

    def test_hash(self):
        """ Ensure we can use two similar sequences in sets.
        """
        self.assertEqual(
            {
                sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1005"),
                sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1005"),
                sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1004"),
            },
            {
                sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1005"),
                sequence.Sequence.fromString("/path/to/a/file.%04d.ext 1001-1004"),
            },
        )

    def test_frameRange(self):
        """ Ensure a FrameRange can be retrieved from a Sequence.
        """
        frameRange = self._sequence.frameRange

        self.assertEqual(
            (1001, 1005, 4, []), (frameRange.start, frameRange.end, frameRange.padding, frameRange.missing,),
        )

    def test_getPathFromFrameNumber(self):
        """ Ensure specific path(s) can be retrieve from a Sequence.
        """
        self.assertEqual(
            (
                self._sequence_basename + "1001.ext",
                self._sequence_basename + "1003.ext",
                self._sequence_basename + "1005.ext",),
            (
                self._sequence.getFramePath(1001),
                self._sequence.getFramePath(1003),
                self._sequence.getFramePath(1005),
            ),
        )

    def test_getPathFromFrameNumber_missingFrame(self):
        """ Ensure a path to a missing frame cannot be retrieved (can be updated later on).
        """
        missingFrameSequence = sequence.Sequence.fromString(
            "/path/to/a/file.%04d.ext 1-5 [3,4]",  # explicitly provide missing frames
        )

        with self.assertRaises(ValueError):
            _ = missingFrameSequence.getFramePath(3)

    def test_getPathFromFrameNumber_invalidFrame(self):
        """ Ensure an invalid frame path cannot be retrieve from a Sequence.
        """
        with self.assertRaises(ValueError):
            _ = self._sequence.getFramePath("not_a_frame_number")

    def test_getPathFromFrameNumber_wrongFrame(self):
        """ Ensure a wrong frame path cannot be retrieve from a Sequence.
        """
        with self.assertRaises(ValueError):
            _ = self._sequence.getFramePath(8)

    def test_missingFrames(self):
        """ Ensure missing frames can be retrieved from a Sequence.
        """
        missingFrameSequence = sequence.Sequence.fromString(
           self._sequence_basename + "%04d.ext 1-5 [3,4]",  # explicitly provide missing frames
        )

        self.assertEqual(
            (
                [
                    self._sequence_basename + "0001.ext",
                    self._sequence_basename + "0002.ext",
                    self._sequence_basename + "0005.ext",
                ],
                [
                    self._sequence_basename + "0003.ext",
                    self._sequence_basename + "0004.ext"
                ],
            ),
            (list(missingFrameSequence), missingFrameSequence.missing,),
        )


class TestSequenceNonZeroPadded(unittest.TestCase):
    """ Test case for sequence that are not zero padded.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(TestSequenceNonZeroPadded, self).setUp()
        self._sequence_str = os.path.abspath(os.path.join(os.sep, "path", "to", "a", "file"))
        self._sequence = sequence.Sequence.fromString(self._sequence_str + ".%d.ext 7-11")

    def test_iter(self):
        """ Ensure sequence can be iterated over.
        """
        self.assertEqual(
            [
                self._sequence_str + ".7.ext",
                self._sequence_str + ".8.ext",
                self._sequence_str + ".9.ext",
                self._sequence_str + ".10.ext",
                self._sequence_str + ".11.ext",
            ],
            list(self._sequence),
        )



class TestSequenceRelative(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.sequence._sequence module from a relative path.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(TestSequenceRelative, self).setUp()
        self._sequence = sequence.Sequence.fromString("file.%04d.ext 1001-1005")

    def test_properties(self):
        """ Ensure the Sequence properties are valid.
        """
        self.assertEqual(
            (
                "file.",
                ".ext",
                os.path.join(os.getcwd(), "file.1001.ext"),
                os.path.join(os.getcwd(), "file.1005.ext"),
                [],
                4,
            ),
            (
                self._sequence.head,
                self._sequence.tail,
                self._sequence.start,
                self._sequence.end,
                self._sequence.missing,
                self._sequence.padding,
            ),
        )

    def test_representation(self):
        """ Ensure a Sequence represents correctly.
        """
        self.assertEqual(
            "<Sequence <FileSequence: 'file.1001-1005#.ext'>>", repr(self._sequence),
        )

    def test_representationAsString(self):
        """ Ensure a Sequence represents correctly as string.
        """
        self.assertEqual(
            "<Sequence 'file.####.ext 1001-1005'>", str(self._sequence),
        )

    def test_iter(self):
        """ Ensure the Sequence can be iterated over.
        """
        self.assertEqual(
            [
                os.path.join(os.getcwd(), "file.1001.ext"),
                os.path.join(os.getcwd(), "file.1002.ext"),
                os.path.join(os.getcwd(), "file.1003.ext"),
                os.path.join(os.getcwd(), "file.1004.ext"),
                os.path.join(os.getcwd(), "file.1005.ext"),
            ],
            list(self._sequence),
        )


class TestSequenceSingleFrame(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.sequence._sequence module from a single frame path.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(TestSequenceSingleFrame, self).setUp()
        self._sequence = sequence.Sequence.fromString("file.%04d.ext 1005-1005")

    def test_properties(self):
        """ Ensure the Sequence properties are valid.
        """
        self.assertEqual(
            (
                "file.",
                ".ext",
                os.path.join(os.getcwd(), "file.1005.ext"),
                os.path.join(os.getcwd(), "file.1005.ext"),
                [],
                4,
            ),
            (
                self._sequence.head,
                self._sequence.tail,
                self._sequence.start,
                self._sequence.end,
                self._sequence.missing,
                self._sequence.padding,
            ),
        )

    def test_headWithMultipleDigits(self):
        """ Ensure we can correctly retrieve the head for a single frame sequence with multiple digits.
        """
        result = sequence.Sequence.fromList(["file_1000_suffix.1001.ext"])

        self.assertEqual(
            (
                "file_1000_suffix.",
                ".ext",
                os.path.join(os.getcwd(), "file_1000_suffix.1001.ext"),
                os.path.join(os.getcwd(), "file_1000_suffix.1001.ext"),
                [],
                4,
            ),
            (result.head, result.tail, result.start, result.end, result.missing, result.padding,),
        )

    def test_representation(self):
        """ Ensure a Sequence represents correctly.
        """
        self.assertEqual(
            "<Sequence <FileSequence: 'file.1005#.ext'>>", repr(self._sequence),
        )

    def test_representationAsString(self):
        """ Ensure a Sequence represents correctly as string.
        """
        self.assertEqual("<Sequence '%s'>" % os.path.join(os.getcwd(), "file.1005.ext"), str(self._sequence))

    def test_frameRange(self):
        """ Ensure the frame range from the sequence is correct.
        """
        frameRange = self._sequence.frameRange

        self.assertEqual(sequence.FrameRange(1005, 1005, padding=4), frameRange)

    def test_iter(self):
        """ Ensure the Sequence can be iterated over.
        """
        self.assertEqual(
            [os.path.join(os.getcwd(), "file.1005.ext"),], list(self._sequence),
        )


class TestSequenceInit(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.sequence._sequence initialization.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(TestSequenceInit, self).setUp()
        self.tempDirectory = tempfile.mkdtemp()

    def tearDown(self):
        """ Tear down the testing class.
        """
        super(TestSequenceInit, self).tearDown()
        shutil.rmtree(self.tempDirectory)

    def test__init__from_FileSequence(self):
        """ Ensure a Sequence can be initialized from a FileSequence object.
        """
        seq_path = os.path.join(os.sep, "dir", "prefix.1-10%04d.ext")
        seq = sequence.Sequence(fileseq.FileSequence(seq_path))
        self.assertEqual(
            ("prefix.", ".ext", 4, 1, 10, True, [],),
            (seq.head, seq.tail, seq.padding, seq.frameRange.start, seq.frameRange.end, seq.hasLeadingZeros, seq.missing),
        )

    def test__init__invalid_sequence(self):
        """ Ensure a Sequence object cannot be initialized from a non-sequence.
        """
        with self.assertRaises(ValueError) as error:
            sequence.Sequence("not_a_sequence")
        self.assertEqual("Cannot initialize a Sequence from 'not_a_sequence'.", str(error.exception))

    def test__init__invalid_fileseq_sequence(self):
        """ Ensure a Sequence object cannot be initialized from a FileSeq sequence without any frame info.
        """
        with self.assertRaises(ValueError) as error:
            sequence.Sequence(fileseq.FileSequence("/a/single/file"))

    def test_fromString_fails(self):
        """ Ensure a Sequence object cannot be initialized from an invalid string.
        """
        with self.assertRaises(ValueError) as error:
            _ = sequence.Sequence.fromString("not_a_string_sequence")
        self.assertEqual("Invalid path: 'not_a_string_sequence'", str(error.exception))

    def test_fromString_no_prefix(self):
        """ Ensure a Sequence object can be initialized from a string with no directory or prefix.
        """
        seq = sequence.Sequence.fromString("%04d.exr 1-10")
        self.assertEqual(("", ".exr"), (seq.head, seq.tail))

    def test_fromString_directory_no_prefix(self):
        """ Ensure a Sequence object can be initialized from a string with a directory and no prefix.
        """
        seq = sequence.Sequence.fromString("/dir/%04d.exr 1-10")
        self.assertEqual(("", ".exr"), (seq.head, seq.tail))

    def test_fromString_no_frame_range(self):
        """ Ensure a Sequence object cannot be initialized from a path without any framerange.
        """
        with self.assertRaises(ValueError) as error:
            sequence.Sequence.fromString("dir/img.####.exr")

        self.assertEqual(
            str(error.exception), "Path have no frame range information: 'dir/img.####.exr'",
        )

    def test_fromString_no_frame_range_allowEmpty(self):
        """ Ensure a Sequence object can be initialized from a path without any frame range when
        the `allowEmpty` flag is used.
        """
        self.assertTrue(sequence.Sequence.fromString("dir/img.####.exr", allowEmpty=True))

    def test_fromList(self):
        """ Ensure a Sequence object can be initialized from a list of path.
        """
        listSequence = sequence.Sequence.fromList(
            [
                "/path/to/a/file_v01.ext",
                "/path/to/a/file_v02.ext",
                "/path/to/a/file_v03.ext",
                "/path/to/another/file_v01.ext",
            ]
        )

        self.assertEqual(3, len(listSequence))

    def test_fromList_singleEntry(self):
        """ Ensure a list of Sequence object can be initialized from a list of path when the
        singleEntry kwarg is set to False.
        """
        listSequence = sequence.Sequence.fromList(
            [
                "/path/to/a/file_v01.ext",
                "/path/to/a/file_v02.ext",
                "/path/to/a/file_v03.ext",
                "/path/to/another/file_v01.ext",
            ],
            singleEntry=False,
        )

        self.assertEqual(len(listSequence), 2)

    def test_fromList_preserveList(self):
        """ Ensure the fromList function doesn't edit the input list.
        """
        files = ["/path/to/a/file_v01.ext"]
        _ = sequence.Sequence.fromList(files)

        self.assertListEqual(files, ["/path/to/a/file_v01.ext"])

    def test_fromListError(self):
        """ Ensure a ValueError is raised if no Sequence object can be initialized from a list of paths.
        """
        with self.assertRaises(ValueError):
            sequence.Sequence.fromList(
                [
                    "/path/to/a/a_single_file.ext",
                    "/path/to/a/another_single_file.ext",
                    "/path/to/a/yet_another_single_file.ext",
                ]
            )

    def test_fromList_sorted(self):
        """ Ensure a Sequence object can be initialized from a random list of path, by sorting it.
        """
        listSequence = sequence.Sequence.fromList(
            ["/path/to/a/file.1001.ext", "/path/to/a/file.1002.ext", "/path/to/a/file.1.ext",]
        )

        self.assertEqual([1, 1001, 1002], list(listSequence.frameRange))

    def test_fromList_ambiguous_leading_zero(self):
        """ Ensure that we don't assume padding in case of ambiguity.
        """
        listSequence = sequence.Sequence.fromList(["/path/to/a/file.1001.exr", "/path/to/a/file.1003.exr",])
        self.assertEqual(False, listSequence.hasLeadingZeros)

    def test_fromList_strRepresentation(self):
        """ Ensure that we cannot resolve a sequence from it's string representation using fromList.
        """
        for listData in (
            ["/path/to/sequence.%04d.exr 1-10"],
            ["/path/to/sequence.%d.exr 1-10"],
            ["/path/to/sequence.(1-10)%04d.exr"],
            ["/path/to/sequence.####.exr 1-10"],
            ["/path/to/sequence.1-10@@@@.exr"],
            # This one would incorrectly be accepted by fileseq.findSequencesInList
            ["/path/to/sequence.0001-0010.exr"],
        ):
            with self.assertRaises(ValueError):
                _ = sequence.Sequence.fromList(listData)

    def test_fromList_no_leading_zero(self):
        """ Ensure a Sequence without leading zeros can be built from a list without leading zeros.
        """
        listSequence = sequence.Sequence.fromList(["/path/to/a/file.9.exr", "/path/to/a/file.11.exr",])
        self.assertEqual(False, listSequence.hasLeadingZeros)

    def test_fromList_leading_zero(self):
        """ Ensure a Sequence with leading zeros canb e built from a list with leading zeros.
        """
        listSequence = sequence.Sequence.fromList(["/path/to/a/file.09.exr", "/path/to/a/file.11.exr",])
        self.assertEqual(True, listSequence.hasLeadingZeros)

    def test_getSequences_fromPath(self):
        """ Ensure a Sequence can be found on disk.
        """
        for index in range(1001, 1003):
            open(os.path.join(self.tempDirectory, "file.%06d.ext" % index), "a").close()  # touch file

        foundSequence, = sequence.Sequence.getSequences(self.tempDirectory)
        self.assertEqual(2, len(foundSequence))

    def test_getSequences_fromPath_missingFrames(self):
        """ Ensure a Sequence with missing frames can be found on disk.
        """
        # sequence 1
        for index in range(1001, 1003):
            open(os.path.join(self.tempDirectory, "file.%06d.ext" % index), "a").close()  # touch file

        # sequence 2
        for index in range(1, 10):
            open(os.path.join(self.tempDirectory, "path.%d.ext" % index), "a").close()  # touch file

        # sequence 3
        for index in range(25, 30):
            open(os.path.join(self.tempDirectory, "seq_%03d.ext" % index), "a").close()  # touch file

        foundSequences = sequence.Sequence.getSequences(self.tempDirectory)
        self.assertEqual(
            (
                3,
                [1001, 1002],
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [25, 26, 27, 28, 29],
            ),
            (
                len(foundSequences),
                list(foundSequences[0].frameRange),
                list(foundSequences[1].frameRange),
                list(foundSequences[2].frameRange),
            )
        )

    def test_getSequences_fromPath_multiple(self):
        """ Ensure multiple Sequences can be found on disk.
        """
        for index in range(1001, 1008, 3):
            open(os.path.join(self.tempDirectory, "file.%06d.ext" % index), "a").close()  # touch file

        (foundSequence,) = sequence.Sequence.getSequences(self.tempDirectory)
        self.assertEqual(
            (
                [1001, 1004, 1007],
                [1002, 1003, 1005, 1006],
            ),
            (
                list(foundSequence.frameRange),
                foundSequence.frameRange.missing,
            ),
        )

    def test_getSequence_fromEmptyList(self):
        """ Ensure no sequences are retrieved from an empty list.
        """
        self.assertEqual(
            [], sequence.Sequence.getSequences([]),
        )

    def test_getSequence_fromList(self):
        """ Ensure multiple sequences can be retrieved from a list of path(s).
        """
        sequences = sequence.Sequence.getSequences(
            [
                "/path/to/a/sequence/file.1.ext",
                "/path/to/a/sequence/file.2.ext",
                "/path/to/a/sequence/file.5.ext",
                "/path/to/another/sequence/file_.1001.ext",
                "/path/to/another/sequence/file_.1002.ext",
                "/path/to/a/file.ext",
            ]
        )

        self.assertEqual(
            [
                sequence.Sequence.fromString("/path/to/a/sequence/file.%d.ext 1-5 ([3, 4])"),
                sequence.Sequence.fromString("/path/to/another/sequence/file_.%04d.ext 1001-1002"),
            ],
            sequences,
        )


class BaseSequenceTestCase(unittest.TestCase):
    """ Base test cases for a sequence.
    """

    def _assertSequenceEquals(self, sequenceStr):
        """ Helper method that compare a provided sequence with another built from a string representation.

        :param str sequenceStr: A sequence string representation
        """
        # pylint: disable=no-member
        self.assertEqual(self.sequence, sequence.Sequence.fromString(sequenceStr, allowEmpty=True))


class MutableSequenceWithoutFrameRangeTest(BaseSequenceTestCase):
    """ Tests for a mutable padded sequence object that don't have a frame range.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(MutableSequenceWithoutFrameRangeTest, self).setUp()
        self.sequence = sequence.Sequence.fromString("/path/to/a.%01d.exr", allowEmpty=True)

    def test_valid_properties(self):
        """ Ensure we can access basic properties.
        """
        for actual, expected in (
            (self.sequence.head, "a."),
            (self.sequence.tail, ".exr"),
            (self.sequence.padding, 1),
            (self.sequence.hasLeadingZeros, False),
            (self.sequence.missing, []),
        ):
            self.assertEqual(expected, actual)

    def test_invalid_properties(self):
        """ Ensure accessing incompatible properties raise an exception.
        """
        for attr in ("start", "end", "frameRange"):
            with self.assertRaises(sequence.NoFrameRangeError) as error:
                getattr(self.sequence, attr)
            self.assertEqual("No frame range information available.", str(error.exception))

    def test_iter(self):
        """ Ensure we ca iterate in a sequence without a frame range.
        """
        self.assertEqual((), tuple(self.sequence))


class MutablePaddedSequenceWithoutFrameRangeTest(BaseSequenceTestCase):
    """ Additional tests for a mutable padded sequence object without any frame range.
    """

    def setUp(self):
        """ Set up the testing class.
        """
        super(MutablePaddedSequenceWithoutFrameRangeTest, self).setUp()
        self.sequence_str = os.path.join("path", "to", "a.%04d.exr")
        self.sequence = sequence.Sequence.fromString(self.sequence_str, allowEmpty=True)

    def test_valid_properties(self):
        """ Ensure we can access basic properties.
        """
        for actual, expected in (
            (self.sequence.head, "a."),
            (self.sequence.tail, ".exr"),
            (self.sequence.padding, 4),
            (self.sequence.hasLeadingZeros, True),
            (self.sequence.missing, []),
        ):
            self.assertEqual(expected, actual)

    def test_invalid_properties(self):
        """ Validate accessing incompatible properties raise an exception.
        """
        for attr in ("start", "end", "frameRange"):
            with self.assertRaises(sequence.NoFrameRangeError) as error:
                getattr(self.sequence, attr)
            self.assertEqual("No frame range information available.", str(error.exception))

    def test_valid_formats(self):
        """ Ensure we can format using non-extended formats.
        """
        for format_, expected in (
            (sequence.PredefinedFormat.SPRINTF, os.path.join("path", "to", "a.%04d.exr")),
            (sequence.PredefinedFormat.LEGACY_HASHTAG, os.path.join("path", "to", "a.####.exr")),
            (sequence.PredefinedFormat.FFMPEG, os.path.join("path", "to", "a.%04d.exr")),
        ):
            self.assertEqual(expected, self.sequence.format(format_))

    def test_invalid_formats(self):
        """ Ensure an exception is raise if we try to format a sequence without frame range using an extended
        predefined format.
        """
        for format_ in (
            sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED,
        ):
            with self.assertRaises(ValueError) as error:
                self.sequence.format(format_)
            self.assertEqual(
                "Could not format sequence without a frame range to an extended format.",
                str(error.exception),
            )
