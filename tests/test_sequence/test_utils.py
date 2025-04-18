""" Test cases for the `lite_media_core.path_utils.sequence._utils.py` module.
"""
import unittest

from lite_media_core.path_utils.sequence._utils import conformPath


class TestConformPath(unittest.TestCase):
    """ Test cases for the `conformPath` method.
    """

    def test_single_frame(self):
        """ Test conforming of a single frame.
        """
        self.assertEqual(conformPath("dir/img.1.exr"), "dir/img.1@.exr")

    def test_single_frame_zero_padded(self):
        """ Test conforming of a zero-padding single frame.
        """
        self.assertEqual(conformPath("dir/img.001.exr"), "dir/img.001@@@.exr")

    def test_single_frame_zero_padding_negative(self):
        """ Test conforming a single zero-padded negative frame.
        """
        self.assertEqual(conformPath("dir/img.-01.exr"), "dir/img.-01@@@.exr")

    def test_multiple_frame_no_padding(self):
        """ Test conforming of multiple frames without any padding info.
        """
        self.assertEqual(conformPath("dir/img.001-010.exr"), "dir/img.001-010@@@.exr")

    def test_sprintf_no_padding_number(self):
        """ Test conforming of a sprintf path with no padding number. ('%d')
        """
        self.assertEqual(conformPath("dir/img.%d.exr"), "dir/img.@.exr")

    def test_sprintf_null_padding_number(self):
        """ Test conforming of a sprintf path with a null padding number. ('%0d')
        """
        self.assertEqual(conformPath("dir/img.%0d.exr"), "dir/img.@.exr")

    def test_dash_no_framerange(self):
        """ Test conforming of a dashed path.
        """
        self.assertEqual(conformPath("dir/img.#.exr"), "dir/img.@.exr")

    def test_3_dashes_no_framerange(self):
        """ Test conforming of a path with 3 dashes.
        """
        self.assertEqual(conformPath("dir/img.###.exr"), "dir/img.@@@.exr")

    def test_4_dashes_no_framerange(self):
        """ Test conforming of a path with 4 dashes.
        """
        self.assertEqual(conformPath("dir/img.####.exr"), "dir/img.#.exr")

    def test_houdini_no_framerange(self):
        """ Test conforming of a houdini path without any frame range.
        """
        self.assertEqual(conformPath("dir/img.$F.exr"), "dir/img.@.exr")

    def test_sprintf_no_framerange(self):
        """ Test conforming of a sprintf path without any frame range.
        """
        self.assertEqual(conformPath("dir/img.%03d.exr"), "dir/img.@@@.exr")

    def test_sprintf_contained_standard_framerange(self):
        """ Test conforming of a sprintf path with a contained standard frame range.
        """
        self.assertEqual(conformPath("dir/img.1-10%03d.exr"), "dir/img.1-10@@@.exr")

    def test_sprintf_extended_standard_framerange(self):
        """ Test conforming of a path with an extended standard frame range.
        """
        self.assertEqual(conformPath("dir/img.%03d.exr 1-3"), "dir/img.1-3@@@.exr")

    def test_sprintf_extended_broken_framerange(self):
        """ Test conforming of a path with an extended broken frame range.
        """
        self.assertEqual(conformPath("dir/img.%03d.exr [1-3, 5, 10]"), "dir/img.1-3,5,10@@@.exr")

    def test_sprintf_extended_broken_framerange_broken_missing(self):
        """ Test conforming of a path with an extended broken frame range and broken missing frames.
        """
        self.assertEqual(
            conformPath("dir/img.%03d.exr [1-8, 10] ([2-3, 7])"), "dir/img.1,4-6,8,10@@@.exr",
        )

    def test_sprintf_contained_framerange_mismatch_padding(self):
        """ Test special case of a path with contained frame range and mismatching padding hint.
        """
        self.assertEqual(conformPath("dir/img.10-11@.exr"), "dir/img.10-11@.exr")  # no hint in frame range

        self.assertEqual(  # padding hint of 1, frame range hint of 2
            conformPath("dir/img.01-10@.exr"), "dir/img.01-10@@.exr"
        )

        self.assertEqual(  # padding hint of 2, frame range hint of 3
            conformPath("dir/img.010-100@@.exr"), "dir/img.010-100@@@.exr"
        )

    def test_sprintf_extended_framerange_mismatch_padding(self):
        """ Test special case of a path with extended frame range and mismatching padding hint.
        """
        self.assertEqual(conformPath("dir/img.@.exr 10-11"), "dir/img.10-11@.exr")  # no hint in frame range

        self.assertEqual(  # padding hint of 1, framer ange hint of 2
            conformPath("dir/img.@.exr 01-10"), "dir/img.01-10@@.exr"
        )

        self.assertEqual(  # padding hint of 2, frame range hint of 3
            conformPath("dir/img.@@.exr 010-100"), "dir/img.010-100@@@.exr"
        )

    def test_invalid_path(self):
        """ Ensure a ValueError is raised when conforming an invalid path.
        """
        with self.assertRaises(ValueError) as error:
            conformPath("dir/not_a_sequence.exr")

        self.assertEqual(str(error.exception), "Invalid path: 'dir/not_a_sequence.exr'")

    def test_invalid_path_contained_and_extended(self):
        """ Ensure a ValueError is raised when conforming a path that use both frame range form.
        """
        with self.assertRaises(ValueError) as error:
            conformPath("dir/img.001-010@.exr 001-010")

        self.assertEqual(
            str(error.exception),
            "Path cannot have both a contained and an extended frame range: "
            "'dir/img.001-010@.exr 001-010'",
        )

    def test_invalid_path_suffix_after_padding(self):
        """ Ensure a ValueError is raised when conforming a path with a padding that don't end with an ext.
        """
        with self.assertRaises(ValueError) as error:
            conformPath("dir/img.%04d_suffix.ext")

        self.assertEqual(str(error.exception), "Invalid path: 'dir/img.%04d_suffix.ext'")
