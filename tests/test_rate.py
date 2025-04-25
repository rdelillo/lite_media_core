""" Test lite_media_core.rate module.
"""
import unittest

from lite_media_core import rate


class TestStandardFrameRate(unittest.TestCase):
    """ Test basic frame rate usage.
    """
    def test_standard_rate_from_float(self):
        """ Ensure a standard frame rate object can be created from a float.
        """
        frameRate = rate.StandardFrameRate(24.0)
        self.assertEqual(
            ("Film", 24.0),
            (frameRate.name, float(frameRate)),
        )

    def test_standard_rate_from_int(self):
        """ Ensure a standard frame rate object can be created from an int.
        """
        frameRate = rate.StandardFrameRate(24)
        self.assertEqual(
            ("Film", 24.0),
            (frameRate.name, float(frameRate)),
        )

    def test_standard_rate_from_str(self):
        """ Ensure a standard frame rate object can be created from a str.
        """
        frameRate = rate.StandardFrameRate("24")
        self.assertEqual(
            ("Film", 24.0),
            (frameRate.name, float(frameRate)),
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
        frameRate = rate.FrameRate(25.0)
        self.assertEqual("25.0 fps", str(frameRate))

    def test_represents(self):
        """ Ensure a standard frame rate can be represented.
        """
        frameRate = rate.StandardFrameRate(50.0)
        self.assertEqual("<StandardFrameRate 50.0 fps HD-TV>", repr(frameRate))

    def test_NtscRounding(self):
        """ Ensure NTSC rounding is correctly handled.
            Standard frame 24.0 fps with NTSC compatibility is technically 24.0*(1000/1001) = 23.976
            but often rounded to 23.98. Need to ensure both frame rate creates the same industry standard.
        """
        frameRate1 = rate.FrameRate(23.976)
        frameRate2 = rate.FrameRate(23.98)

        # Both rates are "Film with NTSC compatibility"
        self.assertEqual(frameRate1.name, frameRate2.name)

    def test_equals_float_True(self):
        """ Ensure a FrameRate object can be compared to a float.
        """
        frameRate = rate.FrameRate(50.0)
        self.assertTrue(frameRate == 50.0)

    def test_equals_float_False(self):
        """ Ensure a FrameRate object wrong comparison with a float return False.
        """
        frameRate = rate.FrameRate(24.0)
        self.assertTrue(frameRate != 1.0)

    def test_equals_fails(self):
        """ Ensure an invalid comparison between FrameRate and other type fails.
        """
        frame_rate = rate.FrameRate(23.98)
        with self.assertRaises(ValueError):
            frame_rate == "value_string"


class TestFrameRate(unittest.TestCase):
    """ Test non-standard frame rate usage.
    """
    def test_create_rate(self):
        """ Ensure a non-standard rate object can be created from the FrameRate factory.
        """
        customRate = rate.FrameRate.from_custom_value(12.0)  # non-standard frame rate
        self.assertTrue(isinstance(customRate, rate.FrameRate))

    def test_representation(self):
        """ Ensure a custom frame rate object can be represented.
        """
        customRate = rate.FrameRate.from_custom_value(33.33)  # non-standard frame rate
        self.assertEqual("<FrameRate 33.33 fps custom rate>", repr(customRate))
