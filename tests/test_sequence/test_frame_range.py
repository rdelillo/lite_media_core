""" Test out the lite_media_core.path_utils.sequence._frameRange module.
"""
import itertools
import unittest

import fileseq

from lite_media_core.path_utils import sequence


class TestFrameRange(unittest.TestCase):
    """ Test out the lite_media_core.path_utils.sequence._frameRange module.
    """

    def test_basicsProperties(self):
        """ Ensure the basic properties can be retrieved from a FrameRange.
        """
        frameRange = sequence.FrameRange(1, 5, padding=4)

        self.assertEqual(
            (1, 5, [], 4), (frameRange.start, frameRange.end, frameRange.missing, frameRange.padding,),
        )

    def test_equality(self):
        """ Ensure two FrameRange objects can be compared as equal.
        """
        frameRange1 = sequence.FrameRange(1, 5, padding=4, missing=[2, 3])
        frameRange2 = sequence.FrameRange(1, 5, padding=4, missing=[2, 3])
        self.assertEqual(frameRange1, frameRange2)

    def test_representation(self):
        """ Ensure a FrameRange represents itself correctly.
        """
        frameRange = sequence.FrameRange(1, 5, padding=4, missing=[2, 3])
        self.assertEqual(
            repr(frameRange), "<FrameRange start=1 end=5 padding=4 step=1 missing=[2, 3]>",
        )

    def test_hash(self):
        """ Ensure a FrameRange is properly hashable.
        """
        frameRange1 = sequence.FrameRange(1, 5, padding=4, missing=[2, 3])
        frameRange2 = sequence.FrameRange(1, 5, padding=4, missing=[2, 3])
        frameRange3 = sequence.FrameRange(1, 10)
        self.assertEqual(2, len({frameRange1, frameRange2, frameRange3}))
        self.assertEqual({frameRange1, frameRange2, frameRange3}, {frameRange1, frameRange3})

    def test_iter(self):
        """ Ensure a FrameRange can be iterated over.
        """
        frameRange = sequence.FrameRange(1, 5, padding=4)
        self.assertEqual([1, 2, 3, 4, 5], list(frameRange))

    def test_iter_missing(self):
        """ Ensure a FrameRange containing missing frames can be iterated over.
        """
        frameRange = sequence.FrameRange(1, 5, padding=4, missing=[2, 3])
        self.assertEqual([1, 4, 5], list(frameRange))

    def test_chunks(self):
        """ Ensure an FrameRange chunks() yield proper results.
        """
        frameRange = sequence.FrameRange(1, 10, padding=4, missing=[2, 3])
        self.assertEqual([(1, 4, 5), (6, 7, 8), (9, 10)], list(frameRange.chunks(3)))

    def test_chunksEmpty(self):
        """ Ensure an empty FrameRange chunks() returns a empty list.
        """
        frameRange = sequence.FrameRange(1, 1, padding=4, missing=[1])
        self.assertEqual([], list(frameRange.chunks(1)))

    def test_chunksInvalid(self):
        """ Ensure invalid inputs will raise a ValueError in chunks().
        """
        with self.assertRaises(ValueError):
            for _ in sequence.FrameRange(1, 2).chunks(0):
                pass

        with self.assertRaises(ValueError):
            for _ in sequence.FrameRange(1, 2).chunks(-2):
                pass

    def test_asString(self):
        """ Ensure a FrameRange can be converted to a frame list string representation.
        """
        frameRange = sequence.FrameRange(1, 10, missing=[3, 4, 6, 7])
        self.assertEqual(str(frameRange), "1-2, 5, 8-10")

    def test_asStringWithStep(self):
        """ Ensure a FrameRange with a step can be converted to a frame list string representation.
        """
        frameRange = sequence.FrameRange(1, 21, step=5, missing=[16])
        self.assertEqual(str(frameRange), "1-11x5, 21")

    def test_asString_stepConsistency(self):
        """ Ensure a FrameRange with a step can be converted to a frame list string representation.
        """
        self.assertEqual(
            str(sequence.FrameRange(1, 101, step=10, missing=[51])), "1-41x10, 61-101x10",
        )
        self.assertEqual(str(sequence.FrameRange(1, 1001, step=50)), "1-1001x50")
        self.assertEqual(str(sequence.FrameRange(1, 14, missing=[5, 6, 7, 11])), "1-4, 8-10, 12-14")

    def test_from_string(self):
        """ Ensure a FrameRange can be created from a frame list string representation.
        """
        frameRange = sequence.FrameRange(1, 10, missing=[3, 4, 6, 7])
        self.assertEqual(sequence.FrameRange.from_string("1-2, 5, 8-10"), frameRange)

    def test_from_string_negative_left(self):
        """ Ensure a FrameRange can be created from a frame list string representation with negative numbers.
        """
        frameRange = sequence.FrameRange(-10, 6)
        self.assertEqual(sequence.FrameRange.from_string("-10-6"), frameRange)

    def test_from_string_negative_left_and_right(self):
        """ Ensure a FrameRange can be created from a frame list string representation with negative numbers.
        """
        frameRange = sequence.FrameRange(-10, -4, missing=[-5])
        self.assertEqual(sequence.FrameRange.from_string("-10--6, -4"), frameRange)

    def test_from_string_step(self):
        """ Ensure a FrameRange can be created with a step from a frame list string representation.
        """
        frameRange = sequence.FrameRange(start=1, end=21, step=5)
        self.assertEqual(sequence.FrameRange.from_string("1-21x5"), frameRange)

    def test_from_string_multipleStepRaise(self):
        """ Ensure FrameRange.from_string() raise if a string provides multiple steps.
        """
        with self.assertRaises(ValueError):
            sequence.FrameRange.from_string("1-21x5, 50-100x10")

    def test_from_stringConsistency(self):
        """ Ensure a FrameRange can be created from various frame range representations.
        """
        self.assertEqual(
            sequence.FrameRange.from_string("1-100"), sequence.FrameRange(start=1, end=100),
        )
        self.assertEqual(sequence.FrameRange.from_string("1"), sequence.FrameRange(start=1, end=1))
        self.assertEqual(
            sequence.FrameRange.from_string("1 50 51"),
            # pylint: disable=range-builtin-not-iterating
            sequence.FrameRange(start=1, end=51, missing=range(2, 50)),
        )

        missing = itertools.chain(range(2, 17), range(18, 51), range(52, 100))
        self.assertEqual(
            sequence.FrameRange.from_string("1, 51, 100-120, 17"),
            sequence.FrameRange(start=1, end=120, missing=missing),
        )

    def test_from_string_stepConsistency(self):
        """ Ensure a FrameRange can be created with steps from various frame range representations.
        """
        self.assertEqual(
            sequence.FrameRange.from_string("1-91x15"), sequence.FrameRange(start=1, end=91, step=15),
        )
        self.assertEqual(
            sequence.FrameRange.from_string("30-50x10, 70"),
            sequence.FrameRange(start=30, end=70, step=10, missing=[60]),
        )
        self.assertEqual(
            sequence.FrameRange.from_string("1-4x1 8-10x1 12-14x1"),
            sequence.FrameRange(start=1, end=14, step=1, missing=[5, 6, 7, 11]),
        )
        self.assertEqual(
            sequence.FrameRange.from_string("1-101x50, 201"),
            sequence.FrameRange(start=1, end=201, step=50, missing=[151]),
        )

    def test_from_string_invalid(self):
        """ Ensure invalid inputs will raise a ValueError in from_string().
        """
        with self.assertRaises(ValueError):
            sequence.FrameRange.from_string("")

        with self.assertRaises(ValueError):
            sequence.FrameRange.from_string("an invalid input")

        with self.assertRaises(ValueError):
            sequence.FrameRange.from_string("x1,4-8,10")  # Does not start with an int

    def test_from_data_single_number(self):
        """ Ensure a FrameRange can be created from a single frame.
        """
        self.assertEqual(sequence.FrameRange.from_data(1), sequence.FrameRange(start=1, end=1))

    def test_from_data_multiple_numbers(self):
        """ Ensure a FrameRange can be created from multiple frames.
        """
        self.assertEqual(
            sequence.FrameRange.from_data(1, 2, 4), sequence.FrameRange(start=1, end=4, missing=[3]),
        )

    def test_from_data_sequence(self):
        """ Ensure a FrameRange can be created from a sequence of frames.
        """
        self.assertEqual(
            sequence.FrameRange.from_data([1, 2, 4]), sequence.FrameRange(start=1, end=4, missing=[3]),
        )

    def test_from_data_string(self):
        """ Ensure a FrameRange can be created from a string representation.
        """
        self.assertEqual(sequence.FrameRange.from_data("1-100"), sequence.FrameRange(start=1, end=100))

    def test_from_data_frameRange(self):
        """ Ensure a FrameRange can be created from another FrameRange.
        """
        self.assertEqual(
            sequence.FrameRange.from_data(sequence.FrameRange(start=1, end=4, missing=[3])),
            sequence.FrameRange(start=1, end=4, missing=[3]),
        )

    def test_from_data_frameSet(self):
        """ Ensure a FrameRange can be created from a fileseq FrameSet.
        """
        self.assertEqual(
            sequence.FrameRange.from_data(fileseq.FrameSet({1, 2, 4})),
            sequence.FrameRange(start=1, end=4, missing=[3]),
        )

    def test_from_data_invalid(self):
        """ Ensure a FrameRange cannot be created from invalid data.
        """
        with self.assertRaises(ValueError):
            sequence.FrameRange.from_data(1.2)

        with self.assertRaises(ValueError):
            sequence.FrameRange.from_data(None)

        with self.assertRaises(ValueError):
            sequence.FrameRange.from_data("")

    def test_iter_ranges_noMissing(self):
        """ Ensure FrameRange.iter_ranges returns parent range when no missing frames.
        """
        frameRange = sequence.FrameRange(10, 20)
        subRanges = list(frameRange.iter_ranges())

        self.assertEqual([frameRange], subRanges)

    def test_iter_ranges_missing(self):
        """ Ensure FrameRange.iter_ranges returns relevant sub-ranges.
        """
        frameRange = sequence.FrameRange(10, 30, missing=[15, 16, 24, 25])
        subRanges = list(frameRange.iter_ranges())
        expected = [sequence.FrameRange(10, 14), sequence.FrameRange(17, 23), sequence.FrameRange(26, 30)]

        self.assertEqual(expected, subRanges)

    def test_iter_ranges_step(self):
        """ Ensure FrameRange.iter_ranges returns relevant sub-ranges with step.
        """
        frameRange = sequence.FrameRange(10, 30, step=2, missing=[14, 24, 26])
        subRanges = list(frameRange.iter_ranges())
        expected = [
            sequence.FrameRange(10, 12, step=2),
            sequence.FrameRange(16, 22, step=2),
            sequence.FrameRange(28, 30, step=2),
        ]

        self.assertEqual(expected, subRanges)

    def test_iter_ranges_padding(self):
        """ Ensure FrameRange.iter_ranges returns relevant sub-ranges with padding.
        """
        frameRange = sequence.FrameRange(10, 20, padding=4, missing=[15, 16])
        subRanges = list(frameRange.iter_ranges())
        expected = [sequence.FrameRange(10, 14, padding=4), sequence.FrameRange(17, 20, padding=4)]

        self.assertEqual(expected, subRanges)
