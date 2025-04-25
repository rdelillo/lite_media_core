""" Test lite_media_core.resolution module.
"""
import unittest

from lite_media_core import rate
from lite_media_core import timecode


class TestTimecode(unittest.TestCase):
    """ Test basic timecode usage.
    """
    def setUp(self):
        """ Set up testing class.
        """
        super(TestTimecode, self).setUp()
        self.frame_rate = rate.FrameRate(24.0)

    def test_timecode_fromStr(self):
        """ Ensure a valid timecode can be created from a timecode string.
        """
        tc = timecode.Timecode("01:00:00:00", self.frame_rate)

        self.assertEqual(
            ("01:00:00:00", 86400, self.frame_rate),
            (str(tc), tc.frames, tc.frame_rate),
        )

    def test_timecode_fromInt(self):
        """ Ensure a valid timecode can be created from an amount of frames.
        """
        tc = timecode.Timecode(86400, self.frame_rate)

        self.assertEqual(
            ("01:00:00:00", 86400, self.frame_rate),
            (str(tc), tc.frames, tc.frame_rate),
        )

    def test_timecode_fromMilliSecondsStr(self):
        """ Ensure a timecode can be created from a 'HH:MM:SS.MSMS' formatted string.
        """
        tc = timecode.Timecode("00:00:00.08", self.frame_rate)

        self.assertEqual(
            ("00:00:00:02", 2, self.frame_rate),
            (str(tc), tc.frames, tc.frame_rate),
        )

    def test_timecode_from_seconds(self):
        """ Ensure a valid timecode can be created from an amount of seconds.
        """
        tc = timecode.Timecode.from_seconds(3600.0, self.frame_rate)
        self.assertEqual("01:00:00:00", str(tc))  # 3600 seconds = 1 hour

    def test_timecode_from_seconds_floatframe_rate(self):
        """ Ensure a valid timecode can be created from an amount of seconds and a float as frame rate.
        """
        tc = timecode.Timecode.from_seconds(3600.0, 24.0)
        self.assertEqual(
            ("01:00:00:00", self.frame_rate),
            (str(tc), tc.frame_rate),
        )

    def test_timecode_fromFloatSeconds(self):
        """ Ensure a valid timecode can be created from an floating amount of seconds.
        """
        tc = timecode.Timecode.from_seconds(3600.12, self.frame_rate)
        self.assertEqual("01:00:00:03", str(tc))  # 0.12 seconds = 3 frames (2.88)

    def test_timecode_representation(self):
        """ Ensure a valid timecode can be represented.
        """
        tc = timecode.Timecode("01:02:03:04", self.frame_rate)
        self.assertEqual("<Timecode '01:02:03:04' rate='24.0 fps'>", repr(tc))

    def test_timecode_asInt(self):
        """ Ensure a valid timecode object can be represented as an int (number of frames).
        """
        tc = timecode.Timecode(50, self.frame_rate)
        self.assertEqual(50, int(tc))

    def test_timecode_asStr(self):
        """ Ensure a valid timecode object can be represented as a str (timecode).
        """
        tc = timecode.Timecode("00:12:34:12", self.frame_rate)
        self.assertEqual("00:12:34:12", str(tc))

    def test_timecode_asSecond(self):
        """ Ensure a valid timecode can be represented as an amount of seconds.
        """
        tc = timecode.Timecode("00:01:00:00", self.frame_rate)
        self.assertEqual(60.0, tc.seconds)  # 1min = 60 seconds

    def test_timecode_fails_wrongValue(self):
        """ Ensure the process fails when trying to initialize a timecode from a wrong value.
        """
        with self.assertRaises(timecode.TimecodeException):
            _ = timecode.Timecode(
                66.6,  # wrong timecode value (not tc, not amount of frames)
                self.frame_rate,
            )

    def test_timecode_fails_wronglyFormattedValue(self):
        """ Ensure the process fails when trying to initialize a timecode from a badly formatted tc value.
        """
        with self.assertRaises(timecode.TimecodeException):
            _ = timecode.Timecode(
                "wrong_str_value_not_a_timecode",
                self.frame_rate,
            )

    def test_timecode_fails_wrongRate(self):
        """ Ensure the process fails when trying to initialize a timecode from a wrong rate.
        """
        with self.assertRaises(timecode.TimecodeException):
            _ = timecode.Timecode(
                "01:00:00:00",
                "wrongframe_rate",
            )


class TesttimecodeComparisons(unittest.TestCase):
    """ Test timecode comparisons.
    """
    def setUp(self):
        """ Initialize testing class.
        """
        super(TesttimecodeComparisons, self).setUp()

        self.tc1 = timecode.Timecode("00:02:00:00", 24)
        self.tc2 = timecode.Timecode("00:01:00:00", 24)

    def test_equals_true(self):
        """ Ensure 2 timecodes equality (true).
        """
        tc1 = timecode.Timecode("00:00:01:00", 24)
        tc2 = timecode.Timecode(24, 24)  # 24 frames, 24fps = 1 second

        self.assertTrue(tc1 == tc2)

    def test_equals_false(self):
        """ Ensure 2 timecodes equality (false).
        """
        tc1 = timecode.Timecode("00:00:01:00", 24)
        tc2 = timecode.Timecode(48, 24)  # 48 frames, 24fps = 2 seconds

        self.assertTrue(tc1 != tc2)

    def test_equals_invalid_value(self):
        """ Ensure 2 timecodes equality (invalid rate comparison).
        """
        tc1 = timecode.Timecode("00:00:01:00", 24)
        tc2 = timecode.Timecode("00:00:01:00", 25)  # different frame rate

        with self.assertRaises(ValueError):
            tc1 == tc2

    def test_equals_invalid_type(self):
        """ Ensure 2 timecodes equality (wrong type comparison).
        """
        tc = timecode.Timecode("00:00:00:00", 24)

        with self.assertRaises(TypeError):
            tc == "wrong_comparison_with_str"

    def test_lower_then_true(self):
        """ Ensure timecode 'lower then' comparison (true).
        """
        self.assertTrue(self.tc2 < self.tc1)

    def test_lower_then_false(self):
        """ Ensure timecode 'lower then' comparison (false).
        """
        self.assertEqual(False, self.tc1 < self.tc2)

    def test_greater_then_true(self):
        """ Ensure timecode 'greater then' comparison (true).
        """
        self.assertTrue(self.tc1 > self.tc2)

    def test_greater_then_false(self):
        """ Ensure timecode 'greater then' comparison (false).
        """
        self.assertEqual(False, self.tc2 > self.tc1)


class TesttimecodeOperations(unittest.TestCase):
    """ Test timecode operations.
    """
    def test_timecode_add(self):
        """ Ensure 2 timecodes can be added.
        """
        tc1 = timecode.Timecode("01:00:00:00", 24.0)
        tc2 = timecode.Timecode("00:01:00:00", 24.0)
        result = tc1 + tc2

        self.assertEqual(
            ("01:01:00:00", 24.0),
            (str(result), float(result.frame_rate)),
        )


class TesttimecodeUtils(unittest.TestCase):
    """ Test timecode utility features.
    """

    def test_is_valid_timecode_str_True(self):
        """ Ensure a valid timecode string can be validated.
        """
        self.assertTrue(timecode.is_valid_timecode_str("00:04:00:00", frame_rate=24))

    def test_is_valid_timecode_str_False(self):
        """ Ensure an invalid timecode string is correctly detected.
        """
        self.assertEqual(False, timecode.is_valid_timecode_str("wrongTc", frame_rate=24))
