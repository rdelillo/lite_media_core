""" Test lite_media_core.rate module.
"""
import unittest
import math

from lite_media_core import rate


class TestStandardFrameRate(unittest.TestCase):
    """ Test basic frame rate usage.
    """
    def test_standard_rate_from_float(self):
        """ Ensure a standard frame rate object can be created from a float.
        """
        frame_rate = rate.StandardFrameRate(24.0)
        self.assertEqual(
            ("Film", 24.0),
            (frame_rate.name, float(frame_rate)),
        )
        self.assertTrue(frame_rate.is_standard)

    def test_standard_rate_from_int(self):
        """ Ensure a standard frame rate object can be created from an int.
        """
        frame_rate = rate.StandardFrameRate(24)
        self.assertEqual(
            ("Film", 24.0),
            (frame_rate.name, float(frame_rate)),
        )

    def test_standard_rate_from_str(self):
        """ Ensure a standard frame rate object can be created from a str.
        """
        frame_rate = rate.StandardFrameRate("24")
        self.assertEqual(
            ("Film", 24.0),
            (frame_rate.name, float(frame_rate)),
        )

    def test_standard_rate_failsIncorrectValue(self):
        """ Ensure a frame rate object init fails when initialized from invalid value.
        """
        with self.assertRaises(rate.FrameRateException):
            _ = rate.StandardFrameRate("incorrect_rate_value")

    def test_standard_rate_failsNonStandard(self):
        """ Ensure a frame rate object init fails when initialized from non-standard rate value.
        """
        with self.assertRaises(rate.FrameRateException):
            _ = rate.StandardFrameRate(33.3)  # non-standard frame rate

    def test_representsAsString(self):
        """ Ensure a standard frame rate can be represented as string.
        """
        frame_rate = rate.FrameRate(25.0)
        self.assertEqual("25.0 fps", str(frame_rate))

    def test_represents(self):
        """ Ensure a standard frame rate can be represented.
        """
        frame_rate = rate.StandardFrameRate(50.0)
        self.assertEqual("<StandardFrameRate 50.0 fps HD-TV>", repr(frame_rate))

    def test_Ntsc_rounding(self):
        """ Ensure NTSC rounding is correctly handled.
            Standard frame 24.0 fps with NTSC compatibility is technically 24.0*(1000/1001) = 23.976
            but often rounded to 23.98. Need to ensure both frame rate creates the same industry standard.
        """
        frame_rate1 = rate.FrameRate(23.976)
        frame_rate2 = rate.FrameRate(23.98)

        # Both rates are "Film with NTSC compatibility"
        self.assertEqual(frame_rate1.name, frame_rate2.name)

    def test_equals_float_True(self):
        """ Ensure a FrameRate object can be compared to a float.
        """
        frame_rate = rate.FrameRate(50.0)
        self.assertTrue(frame_rate == 50.0)

    def test_equals_float_False(self):
        """ Ensure a FrameRate object wrong comparison with a float return False.
        """
        frame_rate = rate.FrameRate(24.0)
        self.assertTrue(frame_rate != 1.0)

    def test_equals_fails(self):
        """ Ensure an invalid comparison between FrameRate and other type fails.
        """
        frame_rate = rate.FrameRate(23.98)
        with self.assertRaises(ValueError):
            frame_rate == "value_string"

    def test_get_industry_standards(self):
        """ Reach defined industry standard rates.
        """
        standards = rate.FrameRate.get_industry_standards()
        self.assertIsInstance(standards, dict)


class TestFrameRate(unittest.TestCase):
    """ Test non-standard frame rate usage.
    """
    def test_create_rate(self):
        """ Ensure a non-standard rate object can be created from the FrameRate factory.
        """
        custom_rate = rate.FrameRate.from_custom_value(12.0)  # non-standard frame rate
        self.assertTrue(isinstance(custom_rate, rate.FrameRate))
        self.assertFalse(custom_rate.is_standard)

    def test_representation(self):
        """ Ensure a custom frame rate object can be represented.
        """
        custom_rate = rate.FrameRate.from_custom_value(33.33)  # non-standard frame rate
        self.assertEqual("<FrameRate 33.33 fps custom rate>", repr(custom_rate))

    def test_from_custom_value_invalid_inputs(self):
        """ Ensure from_custom_value method with invalid inputs (non-numeric, None, NaN, infinity).
        """
        # Invalid non-numeric string
        with self.assertRaises(rate.FrameRateException):
            rate.FrameRate.from_custom_value("not_a_number")

        # Invalid None input
        with self.assertRaises(rate.FrameRateException):
            rate.FrameRate.from_custom_value(None)

        # Edge case: NaN input
        with self.assertRaises(rate.FrameRateException):
            rate.FrameRate.from_custom_value(math.nan)

        # Edge case: Infinity input
        with self.assertRaises(rate.FrameRateException):
            rate.FrameRate.from_custom_value(math.inf)