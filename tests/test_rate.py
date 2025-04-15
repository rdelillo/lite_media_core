""" Test lite_media_core.rate module.
"""
import unittest

from lite_media_core import rate


class TestFrameRate(unittest.TestCase):
    """ Test basic frame rate usage.
    """
    def test_standardRate_fromFloat(self):
        """ Ensure a standard frame rate object can be created from a float.
        """
        frameRate = rate.FrameRate(24.0)
        self.assertEqual(
            ("Film", 24.0),
            (frameRate.name, float(frameRate)),
        )

    def test_standardRate_fromInt(self):
        """ Ensure a standard frame rate object can be created from an int.
        """
        frameRate = rate.FrameRate(24)
        self.assertEqual(
            ("Film", 24.0),
            (frameRate.name, float(frameRate)),
        )

    def test_standardRate_fromStr(self):
        """ Ensure a standard frame rate object can be created from a str.
        """
        frameRate = rate.FrameRate("24")
        self.assertEqual(
            ("Film", 24.0),
            (frameRate.name, float(frameRate)),
        )

    def test_standardRate_failsIncorrectValue(self):
        """ Ensure a frame rate object init fails when initialized from invalid value.
        """
        self.assertRaises(
            rate.FrameRateException,
            rate.FrameRate,
            "incorrectRateValue",  # invalid frame rate
        )

    def test_standardRate_failsNonStandard(self):
        """ Ensure a frame rate object init fails when initialized from non-standard rate value.
        """
        self.assertRaises(
            rate.FrameRateException,
            rate.FrameRate,
            33.3,  # non-standard frame rate
        )

    def test_representsAsString(self):
        """ Ensure a standard frame rate can be represented as string.
        """
        frameRate = rate.FrameRate(25.0)
        self.assertEqual("25.0 fps", str(frameRate))

    def test_represents(self):
        """ Ensure a standard frame rate can be represented.
        """
        frameRate = rate.FrameRate(50.0)
        self.assertEqual("<FrameRate 50.0 fps HD-TV>", repr(frameRate))

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
        frameRate = rate.FrameRate(23.98)
        self.assertRaises(
            ValueError,
            frameRate.__eq__,
            "wrongComparison",
        )


class TestCustomFrameRate(unittest.TestCase):
    """ Test custom frame rate usage.
    """
    def test_createCustomRate(self):
        """ Ensure a custom frame rate object can be created from the FrameRate factory.
        """
        customRate = rate.FrameRate.fromCustomRate(12.0)  # non-standard frame rate
        self.assertTrue(isinstance(customRate, rate.CustomFrameRate))

    def test_representation(self):
        """ Ensure a custom frame rate object can be represented.
        """
        customRate = rate.FrameRate.fromCustomRate(33.33)  # non-standard frame rate
        self.assertEqual("<CustomFrameRate 33.33 fps custom rate>", repr(customRate))
