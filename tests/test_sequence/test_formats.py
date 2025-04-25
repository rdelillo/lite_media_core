""" Test out the lite_media_core.path_utils formats.
"""
import unittest

from lite_media_core.path_utils import sequence


class TestSequenceFromFormat(unittest.TestCase):
    """ Ensure a lite_media_core.path_utils.sequence.Sequence can created from various string format.
    """

    def test_from_common(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("sequence.%04d.ext 1-5")

        self.assertEqual(
            ("sequence.", 1, 5, ".ext", 4),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_spaces_filename(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequ en ce.1-5#.ext")

        self.assertEqual(
            ("sequ en ce.", 1, 5, ".ext", 1),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_spaces_dirname(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a /sequence.1-5#.ext")

        self.assertEqual(
            ("sequence.", 1, 5, ".ext", 1),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_spaces(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a /sequ ence.1-5#.ext")

        self.assertEqual(
            ("sequ ence.", 1, 5, ".ext", 1),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_padded(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.0001-0005.ext")

        self.assertEqual(
            ("sequence.", 1, 5, ".ext", 4),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_noPad(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.1-10#.ext")

        self.assertEqual(
            ("sequence.", 1, 10, ".ext", 2),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_noPad_2(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.%d.ext 0-10")

        self.assertEqual(
            ("sequence.", 0, 10, ".ext", 2, False),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding, result.has_leading_zeros),
        )

    def test_from_common_noPad_3(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.%0d.ext 1-10")

        self.assertEqual(
            ("sequence.", 1, 10, ".ext", 2, False),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding, result.has_leading_zeros),
        )

    def test_from_common_versionAndFrame(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence_v40.0-1@@@@.ext")

        self.assertEqual(
            (
                "sequence_v40.",
                0,
                1,
                ".ext",
                4,
                True,
            ),
            (
                result.head,
                result.frame_range.start,
                result.frame_range.end,
                result.tail, result.padding,
                result.has_leading_zeros,
            ),
        )

    def test_from_common_zfillPadded(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("sequence.0800-0805#.ext")

        self.assertEqual(
            (
                "sequence.",
                800,
                805,
                ".ext",
                4,
                "sequence.%04d.ext",
                True,
            ),
            (
                result.head,
                result.frame_range.start,
                result.frame_range.end,
                result.tail,
                result.padding,
                result.format(sequence.PredefinedFormat.FFMPEG),
                result.has_leading_zeros,
            ),
        )

    def test_from_common_frameDelimiterSwitch(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.799-805@@@@.ext")

        self.assertEqual(
            (
                "sequence.",
                799,
                805,
                ".ext",
                4,
            ),
            (
                result.head,
                result.frame_range.start,
                result.frame_range.end,
                result.tail,
                result.padding,
            ),
        )

    def test_from_common_pointDelimiter(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.1001-1005.ext")

        self.assertEqual(
            ("sequence.", 1001, 1005, ".ext", 4),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_underscoreDelimiter(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence_1-5.ext")

        self.assertEqual(
            ("sequence_", 1, 5, ".ext", 1),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_multiple_extensions_contained(self):
        """ Ensure a Sequence object can be created from a contained sequence string with multiple extensions.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence_1-5.bgeo.sc")

        self.assertEqual(
            ("sequence_", 1, 5, ".bgeo.sc", 1),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_common_multiple_extensions_extended(self):
        """ Ensure a Sequence object can be created from an extended sequence string with multiple extensions.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence_%d.bgeo.sc 1-5")

        self.assertEqual(
            ("sequence_", 1, 5, ".bgeo.sc", 1),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_singleFrame(self):
        """ Ensure a Sequence object can be created from a string.
        """
        result = sequence.Sequence.from_string("sequence.%04d.ext 1-1")

        self.assertEqual(
            ("sequence.", 1, 1, ".ext", 4),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_missingFrames(self):
        """ Ensure a Sequence object can be created from a 'missing frame' string.
        """
        result = sequence.Sequence.from_string("sequence.%04d.ext 1-10 ([2,7,8])")

        self.assertEqual(
            (
                "sequence.",
                [1, 3, 4, 5, 6, 9, 10],
                ".ext",
                4,
                [2, 7, 8],
            ),
            (result.head, list(result.frame_range), result.tail, result.padding, result.frame_range.missing),
        )

    def test_explicitframe_range(self):
        """ Ensure a Sequence object can be created from a 'explicit frame range' string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.%04d.ext [1-2, 9-10]")

        self.assertEqual(
            (
                "sequence.",
                1,
                10,
                ".ext",
                4,
                [3, 4, 5, 6, 7, 8]
            ),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding, result.frame_range.missing),
        )

    def test_from_legacy_player_explicit(self):
        """ Ensure a Sequence object can be created from an alternative formatted string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.####.ext 1-5")

        self.assertEqual(
            ("sequence.", 1, 5, ".ext", 4),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )

    def test_from_alternative_explicit_digits(self):
        """ Ensure a Sequence object can be created from an alternative formatted string.
        """
        result = sequence.Sequence.from_string("/path/to/a/sequence.@@@.ext 1-5")

        self.assertEqual(
            ("sequence.", 1, 5, ".ext", 3),
            (result.head, result.frame_range.start, result.frame_range.end, result.tail, result.padding),
        )


class TestFormatSequence(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.sequence.Sequence can be formatted correctly.
    """

    def setUp(self):
        """ Set up testing class.
        """
        super(TestFormatSequence, self).setUp()
        self._sequence = sequence.Sequence.from_string("sequence.1001-1002#.ext")

    def test_predefined_ffmpeg(self):
        """ Ensure the sequence can be formatted to the string FFmpeg format.
        """
        self.assertEqual(
            "sequence.%d.ext", self._sequence.format(sequence.PredefinedFormat.FFMPEG),
        )

    def test_predefined_sprintf(self):
        """ Ensure the sequence can be formatted to the string Houdini format.
        """
        self.assertEqual(
            "sequence.%d.ext", self._sequence.format(sequence.PredefinedFormat.SPRINTF),
        )

    def test_predefined_legacy_hashtag(self):
        """ Ensure the sequence can be formatted to the legacy hashtag format.
        """
        self.assertEqual(
            "sequence.####.ext", self._sequence.format(sequence.PredefinedFormat.LEGACY_HASHTAG),
        )

    def test_predefined_legacy_hashtag_extended(self):
        """ Ensure the sequence can be formatted to the legacy hashtag format.
        """
        self.assertEqual(
            "sequence.####.ext 1001-1002",
            self._sequence.format(sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED),
        )

    def test_invalid_format(self):
        """ Ensure an exception is raised when trying to use an invalid value.
        """
        with self.assertRaises(ValueError) as error:
            self._sequence.format("an_invalid_format")

        self.assertEqual("Unsupported format: an_invalid_format.", str(error.exception))


class TestFormatSequenceLeadingZeros(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.sequence.Sequence with leading zeros can be formatted correctly.
    """

    def setUp(self):
        """ Set up testing class.
        """
        super(TestFormatSequenceLeadingZeros, self).setUp()
        self._sequence = sequence.Sequence.from_string("sequence.0998-1002#.ext")

    def test_predefined_ffmpeg(self):
        """ Ensure the sequence can be formatted to the string FFmpeg format.
        """
        self.assertEqual(
            "sequence.%04d.ext", self._sequence.format(sequence.PredefinedFormat.FFMPEG),
        )

    def test_predefined_sprintf(self):
        """ Ensure the sequence can be formatted to the string Houdini format.
        """
        self.assertEqual(
            "sequence.%04d.ext", self._sequence.format(sequence.PredefinedFormat.SPRINTF),
        )

    def test_predefined_legacy_hashtag(self):
        """ Ensure the sequence can be formatted to the legacy hashtag format.
        """
        self.assertEqual(
            "sequence.####.ext", self._sequence.format(sequence.PredefinedFormat.LEGACY_HASHTAG),
        )

    def test_predefined_legacy_hashtag_extended(self):
        """ Ensure the sequence can be formatted to the legacy hashtag format.
        """
        self.assertEqual(
            "sequence.####.ext 998-1002",
            self._sequence.format(sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED),
        )
