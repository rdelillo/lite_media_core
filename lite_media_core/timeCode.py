""" Timecode handling.
"""
from typing import Union

import math
import re
import timecode as tcLib  # external lib

from lite_media_core import rate


class TimecodeException(Exception):
    """ Resolution specific exception.
    """


class TimeCode:
    """ Timecode handling.
    """

    def __init__(self, value: Union[str, int], frame_rate: Union[float, int, str, rate.FrameRate]):
        """ Initialize a new Timecode object.

        :raise TimecodeException: When the input parameters are incorrect.
        """
        value, self._frame_rate = _check_tc_parameters(value, frame_rate)

        # tcLib takes only frame rate such as '23.98', '24', '25', '29.97', '30', '50', '59.94' and '60'
        tcLib_frame_rate = str(float(self._frame_rate)).replace(".0", "")

        # Technically this class is a wrap over an external 'timecode' library. This helps to provide a
        # consistent interface with other modules of lite_media_core. Also since this external library is not
        # perfect, we could later on extend/replace the whole timecode logic here.
        # Caveats from external library:
        # - only support industry standard frame rates
        # - different round logic with frames, (01:00:00:00, 24fps) = 86400 frames here (lib returns 86401)
        # - no millisecond based timecode
        # - no unit tests
        if isinstance(value, str):
            self._timecode = tcLib.Timecode(tcLib_frame_rate, start_timecode=value)
            tc_as_frames = math.ceil(self.seconds * float(self._frame_rate))  # 1.01 frame is 2 frames
            self._frames = int(tc_as_frames)
        else:

            # The timecode external library is based such as the 'frames' attribute is the next 'playable'
            # frame and not the timecode time value converted as a number of frame:
            # >>> tc = timecode.Timecode("24", frames=1)
            # >>> str(tc)
            # '00:00:00:00'
            # Hence we compensate the external lib logic by adding an extra frame to the timecode object:
            # >>> tcCompensated = timecode.Timecode("24", frames=1)
            # >>> tcCompensated.add_frames(1)
            # >>> str(tcCompensated)
            # '00:00:00:01'
            self._timecode = tcLib.Timecode(tcLib_frame_rate, frames=value)
            self._timecode.add_frames(1)
            self._frames = value

    def __str__(self) -> str:
        """ Format current Timecode object as a string.
        """
        return str(self._timecode)

    def __repr__(self) -> str:
        """ Represent current Timecode object.
        """
        return "<%s '%s' rate='%s'>" % (self.__class__.__name__, self, self._frame_rate)

    def __int__(self) -> int:
        """ Represent current Timecode object as int.
        """
        return self.frames

    def __eq__(self, other: object) -> bool:
        """ Is equal ?
        """
        self.__checkTypeOnTcOperation(other)
        return int(self) == int(other)

    def __ne__(self, other: object) -> bool:
        """ Is not equal ?
        """
        return not self == other

    def __lt__(self, other: object) -> bool:
        """ Override the default "lower then" behavior.
        """
        self.__checkTypeOnTcOperation(other)
        return int(self) < int(other)

    def __gt__(self, other: object) -> bool:
        """ Override the default "greater then" behavior.
        """
        self.__checkTypeOnTcOperation(other)
        return int(self) > int(other)

    def __add__(self, other: object):
        """ Override the default "add" behavior.

        :param object other: An object to add with current one.
        :return: The result of the addition operation.
        :rtype: :class:`TimeCode`
        """
        self.__checkTypeOnTcOperation(other)
        return TimeCode(int(self) + int(other), self._frame_rate)

    def __checkTypeOnTcOperation(self, other):
        """

        :param object other: The object to check.
        :raise TypeError: When other is not a Timecode object.
        :raise ValueError: When other has a different frame rate.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Invalid operation between Timecode and %r." % object)

        # Does not handle frame rate conform yet.
        if self.frame_rate != other.frame_rate:
            raise ValueError("Cannot compare timecodes with different frame rates %r." % other.frame_rate)

    @property
    def frames(self) -> int:
        """ The timecode as a number of frames.
        """
        return self._frames

    @property
    def seconds(self) -> float:
        """ The timecode as a total number of seconds.
        """
        return sum((
            3600 * self._timecode.hrs,
            60 * self._timecode.mins,
            self._timecode.secs,
            self._timecode.frs / float(self.frame_rate),
        ))

    @property
    def frame_rate(self) -> rate.FrameRate:
        """ The timecode frame rate.
        """
        return self._frame_rate

    @classmethod
    def from_seconds(cls, value_seconds: float, frame_rate: Union[int, float, rate.FrameRate]):
        """ Create a new Timecode object from a time in seconds.

        :param float valueInSeconds: The timecode duration as seconds.
        :param frameRate: the timecode frame rate.
        :type frameRate: float or int or long or str or :class:`lite_media_core.rate.FrameRate`
        :return: The Timecode object.
        :rtype: :class:`Timecode`
        """
        if not isinstance(frame_rate, (rate.FrameRate, rate.NonStandardFrameRate)):
            frame_rate = rate.FrameRate(frame_rate)

        value_frames = math.ceil(value_seconds * float(frame_rate))
        return cls(int(value_frames), frame_rate)


def _check_tc_parameters(tc_value: Union[str, int], tc_rate: Union[float, int, rate.FrameRate]) -> tuple:
    """ Ensure timecode parameters are with correct type.

    :raise TimecodeException: When the input parameters are incorrect.
    """
    if not isinstance(tc_value, (int, str)):
        raise TimecodeException(f"Invalid timecode value {tc_value}, should be int or str.")

    if not isinstance(tc_rate, (rate.FrameRate, rate.NonStandardFrameRate)):
        try:
            tc_rate = rate.FrameRate.fromCustomRate(tc_rate)

        except rate.FrameRateException as error:
            raise TimecodeException("Invalid frame rate for timecode: %s." % error) from error

    if isinstance(tc_value, str) and not is_valid_timecode_str(tc_value, frame_rate=tc_rate):

        # Attempt to convert the timecode string from a milliseconds based formatting.
        try:
            tc_value = _conform_millisecond_timecode(tc_value, tc_rate)

        except ValueError as error:
            raise TimecodeException(
                f"Invalid timecode value {tc_value}, not a valid timecode str syntax."
            ) from error

    return tc_value, tc_rate


def _conform_millisecond_timecode(tc_string: str, frame_rate: rate.FrameRate) -> str:
    """ Conform a 'HH:MM:SS.MSMS' timecode string to 'HH:MM:SS:FF'.
    """
    valid_timecode, milliseconds = tc_string.split(".")
    tc = TimeCode.fromSeconds(float("0.%s" % milliseconds), frame_rate)
    return valid_timeCode + ":%02d" % tc.frames


def is_valid_timecode_str(tc_string: str, frame_rate: float = 24.0) -> bool:
    """ Check if a timecode string is valid according to a certain rate.
    """
    try:
        # Note, tcLib handles milliseconds based timecode since 1.2.0,
        # but math logic seems wrong:
        # test = tcLib.Timecode(24.0, '00:00:00.08')  80 milliseconds ~ 2 frames
        # test.frs = '0.083'
        # so force internal computation.
        MILLISECS_REGEX = r"\d\d:\d\d:\d\d\.[\d]*"
        if re.match(MILLISECS_REGEX, tc_string):
            raise ValueError("Milliseconds-based timecode string")

        # Default tcLib check.
        tcLib.Timecode(float(frame_rate), start_timecode=tc_string)
        return True

    except ValueError:
        return False
