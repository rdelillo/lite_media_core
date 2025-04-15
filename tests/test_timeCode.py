""" Test lite_media_core.resolution module.
"""
import unittest

from lite_media_core import rate
from lite_media_core import timeCode


class TestTimeCode(unittest.TestCase):
    """ Test basic timecode usage.
    """
    def setUp(self):
        """ Set up testing class.
        """
        super(TestTimeCode, self).setUp()
        self.frameRate = rate.FrameRate(24.0)

    def test_timecode_fromStr(self):
        """ Ensure a valid timecode can be created from a timecode string.
        """
        tc = timeCode.TimeCode("01:00:00:00", self.frameRate)

        self.assertEqual(
            ("01:00:00:00", 86400, self.frameRate),
            (str(tc), tc.frames, tc.frameRate),
        )

    def test_timecode_fromInt(self):
        """ Ensure a valid timecode can be created from an amount of frames.
        """
        tc = timeCode.TimeCode(86400, self.frameRate)

        self.assertEqual(
            ("01:00:00:00", 86400, self.frameRate),
            (str(tc), tc.frames, tc.frameRate),
        )

    def test_timecode_fromMilliSecondsStr(self):
        """ Ensure a timecode can be created from a 'HH:MM:SS.MSMS' formatted string.
        """
        tc = timeCode.TimeCode("00:00:00.08", self.frameRate)

        self.assertEqual(
            ("00:00:00:02", 2, self.frameRate),
            (str(tc), tc.frames, tc.frameRate),
        )

    def test_timecode_fromSeconds(self):
        """ Ensure a valid timecode can be created from an amount of seconds.
        """
        tc = timeCode.TimeCode.fromSeconds(3600.0, self.frameRate)
        self.assertEqual("01:00:00:00", str(tc))  # 3600 seconds = 1 hour

    def test_timecode_fromSeconds_floatFrameRate(self):
        """ Ensure a valid timecode can be created from an amount of seconds and a float as frame rate.
        """
        tc = timeCode.TimeCode.fromSeconds(3600.0, 24.0)
        self.assertEqual(
            ("01:00:00:00", self.frameRate),
            (str(tc), tc.frameRate),
        )

    def test_timecode_fromFloatSeconds(self):
        """ Ensure a valid timecode can be created from an floating amount of seconds.
        """
        tc = timeCode.TimeCode.fromSeconds(3600.12, self.frameRate)
        self.assertEqual("01:00:00:03", str(tc))  # 0.12 seconds = 3 frames (2.88)

    def test_timecode_representation(self):
        """ Ensure a valid timecode can be represented.
        """
        tc = timeCode.TimeCode("01:02:03:04", self.frameRate)
        self.assertEqual("<TimeCode '01:02:03:04' rate='24.0 fps'>", repr(tc))

    def test_timecode_asInt(self):
        """ Ensure a valid timecode object can be represented as an int (number of frames).
        """
        tc = timeCode.TimeCode(50, self.frameRate)
        self.assertEqual(50, int(tc))

    def test_timecode_asStr(self):
        """ Ensure a valid timecode object can be represented as a str (timecode).
        """
        tc = timeCode.TimeCode("00:12:34:12", self.frameRate)
        self.assertEqual("00:12:34:12", str(tc))

    def test_timecode_asSecond(self):
        """ Ensure a valid timecode can be represented as an amount of seconds.
        """
        tc = timeCode.TimeCode("00:01:00:00", self.frameRate)
        self.assertEqual(60.0, tc.seconds)  # 1min = 60 seconds

    def test_timecode_fails_wrongValue(self):
        """ Ensure the process fails when trying to initialize a timecode from a wrong value.
        """
        self.assertRaises(
            timeCode.TimecodeException,
            timeCode.TimeCode,
            66.6,  # wrong timecode value (not tc, not amount of frames)
            self.frameRate,
        )

    def test_timecode_fails_wronglyFormattedValue(self):
        """ Ensure the process fails when trying to initialize a timecode from a badly formatted tc value.
        """
        self.assertRaises(
            timeCode.TimecodeException,
            timeCode.TimeCode,
            "wrongTimecodeValue",  # str input but not a timecode format
            self.frameRate,
        )

    def test_timecode_fails_wrongRate(self):
        """ Ensure the process fails when trying to initialize a timecode from a wrong rate.
        """
        self.assertRaises(
            timeCode.TimecodeException,
            timeCode.TimeCode,
            "01:00:00:00",
            "wrongFrameRate",  # wrong frame rate value
        )


class TestTimecodeComparisons(unittest.TestCase):
    """ Test timecode comparisons.
    """
    def setUp(self):
        """ Initialize testing class.
        """
        super(TestTimecodeComparisons, self).setUp()

        self.tc1 = timeCode.TimeCode("00:02:00:00", 24)
        self.tc2 = timeCode.TimeCode("00:01:00:00", 24)

    def test_equals_True(self):
        """ Ensure 2 timecodes equality (true).
        """
        tc1 = timeCode.TimeCode("00:00:01:00", 24)
        tc2 = timeCode.TimeCode(24, 24)  # 24 frames, 24fps = 1 second

        self.assertTrue(tc1 == tc2)

    def test_equals_False(self):
        """ Ensure 2 timecodes equality (false).
        """
        tc1 = timeCode.TimeCode("00:00:01:00", 24)
        tc2 = timeCode.TimeCode(48, 24)  # 48 frames, 24fps = 2 seconds

        self.assertTrue(tc1 != tc2)

    def test_equals_invalidValue(self):
        """ Ensure 2 timecodes equality (invalid rate comparison).
        """
        tc1 = timeCode.TimeCode("00:00:01:00", 24)
        tc2 = timeCode.TimeCode("00:00:01:00", 25)  # different frame rate

        self.assertRaises(ValueError, tc1.__eq__, tc2)

    def test_equals_invalidType(self):
        """ Ensure 2 timecodes equality (wrong type comparison).
        """
        tc = timeCode.TimeCode("00:00:00:00", 24)
        self.assertRaises(TypeError, tc.__eq__, "wrong")  # compare with a string

    def test_lowerThen_True(self):
        """ Ensure timecode 'lower then' comparison (true).
        """
        self.assertTrue(self.tc2 < self.tc1)

    def test_lowerThen_False(self):
        """ Ensure timecode 'lower then' comparison (false).
        """
        self.assertEqual(False, self.tc1 < self.tc2)

    def test_greaterThen_True(self):
        """ Ensure timecode 'greater then' comparison (true).
        """
        self.assertTrue(self.tc1 > self.tc2)

    def test_greaterThen_False(self):
        """ Ensure timecode 'greater then' comparison (false).
        """
        self.assertEqual(False, self.tc2 > self.tc1)


class TestTimecodeOperations(unittest.TestCase):
    """ Test timecode operations.
    """
    def test_timecode_add(self):
        """ Ensure 2 timecodes can be added.
        """
        tc1 = timeCode.TimeCode("01:00:00:00", 24.0)
        tc2 = timeCode.TimeCode("00:01:00:00", 24.0)
        result = tc1 + tc2

        self.assertEqual(
            ("01:01:00:00", 24.0),
            (str(result), float(result.frameRate)),
        )


class TestTimecodeUtils(unittest.TestCase):
    """ Test timecode utility features.
    """

    def test_isValidTimecodeStr_True(self):
        """ Ensure a valid timecode string can be validated.
        """
        self.assertTrue(timeCode.isValidTimecodeStr("00:04:00:00", frameRate=24))

    def test_isValidTimecodeStr_False(self):
        """ Ensure an invalid timecode string is correctly detected.
        """
        self.assertEqual(False, timeCode.isValidTimecodeStr("wrongTc", frameRate=24))
