""" Timecode handling.
"""
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
    def __init__(self, value, frameRate):
        """ Initialize a new Timecode object.

        :param value: The timecode string value or the amount of frames.
        :type value: str or int
        :param frameRate: The timecode frame rate.
        :type frameRate: float or int or long or str or :class:`lite_media_core.rate.FrameRate`
        :raise TimecodeException: When the input parameters are incorrect.
        """
        value, self._frameRate = _checkTcParameters(value, frameRate)

        # tcLib takes only frame rate such as '23.98', '24', '25', '29.97', '30', '50', '59.94' and '60'
        tcLibFrameRate = str(float(self._frameRate)).replace(".0", "")

        # Technically this class is a wrap over an external 'timecode' library. This helps to provide a
        # consistent interface with other modules of lite_media_core. Also since this external library is not
        # perfect, we could later on extend/replace the whole timecode logic here.
        # Caveats from external library:
        # - only support industry standard frame rates
        # - different round logic with frames, (01:00:00:00, 24fps) = 86400 frames here (lib returns 86401)
        # - no millisecond based timecode
        # - no unit tests
        if isinstance(value, str):
            self._timecode = tcLib.Timecode(tcLibFrameRate, start_timecode=value)
            tcAsframes = math.ceil(self.seconds * float(self._frameRate))  # 1.01 frame is 2 frames
            self._frames = int(tcAsframes)
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
            self._timecode = tcLib.Timecode(tcLibFrameRate, frames=value)
            self._timecode.add_frames(1)
            self._frames = value

    def __str__(self):
        """ Represent current Timecode object as a string.

        :return: The string representation.
        :rtype: str
        """
        return str(self._timecode)

    def __repr__(self):
        """ Represent current Timecode object.

        :return: The object representation.
        :rtype: str
        """
        return "<%s '%s' rate='%s'>" % (self.__class__.__name__, self, self._frameRate)

    def __int__(self):
        """ Represent current Timecode object as int.

        :return: The int representation.
        :rtype: int
        """
        return self.frames

    def __eq__(self, other):
        """ Override the default "equals" behavior.

        :param object other: An object to compare against.
        :return: is equal to other object.
        :rtype: bool
        """
        self.__checkTypeOnTcOperation(other)
        return int(self) == int(other)

    def __ne__(self, other):
        """ Override the default "not equals" behavior.

        :param object other: An object to compare against.
        :return: is not equal to other object.
        :rtype: bool
        """
        return not self == other

    def __lt__(self, other):
        """ Override the default "lower then" behavior.

        :param object other: An object to compare against.
        :return: is lower then other object.
        :rtype: bool
        """
        self.__checkTypeOnTcOperation(other)
        return int(self) < int(other)

    def __gt__(self, other):
        """ Override the default "greater then" behavior.

        :param object other: An object to compare against.
        :return: is greater then other object.
        :rtype: bool
        """
        self.__checkTypeOnTcOperation(other)
        return int(self) > int(other)

    def __add__(self, other):
        """ Override the default "add" behavior.

        :param object other: An object to add with current one.
        :return: The result of the addition operation.
        :rtype: :class:`TimeCode`
        """
        self.__checkTypeOnTcOperation(other)
        return TimeCode(int(self) + int(other), self.frameRate)

    def __checkTypeOnTcOperation(self, other):
        """

        :param object other: The object to check.
        :raise TypeError: When other is not a Timecode object.
        :raise ValueError: When other has a different frame rate.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Invalid operation between Timecode and %r." % object)

        # Does not handle frame rate conform yet.
        if self.frameRate != other.frameRate:
            raise ValueError("Cannot compare timecodes with different frame rates %r." % other.frameRate)

    @property
    def frames(self):
        """
        :return: The timecode as a number of frames.
        :rtype: int
        """
        return self._frames

    @property
    def seconds(self):
        """
        :return: The timecode as a total number of seconds.
        :rtype: float
        """
        return sum((
            3600 * self._timecode.hrs,
            60 * self._timecode.mins,
            self._timecode.secs,
            self._timecode.frs / float(self._frameRate),
        ))

    @property
    def frameRate(self):
        """
        :return: The timecode frame rate.
        :rtype: :class: `lite_media_core.rate.FrameRate`
        """
        return self._frameRate

    @classmethod
    def fromSeconds(cls, valueInSeconds, frameRate):
        """ Create a new Timecode object from a time in seconds.

        :param float valueInSeconds: The timecode duration as seconds.
        :param frameRate: the timecode frame rate.
        :type frameRate: float or int or long or str or :class:`lite_media_core.rate.FrameRate`
        :return: The Timecode object.
        :rtype: :class:`Timecode`
        """
        if not isinstance(frameRate, (rate.FrameRate, rate.NonStandardFrameRate)):
            frameRate = rate.FrameRate(frameRate)

        valueInFrames = math.ceil(valueInSeconds * float(frameRate))
        return cls(int(valueInFrames), frameRate)


def _checkTcParameters(tcValue, tcRate):
    """ Ensure timecode parameters are with correct type.

    :param tcValue: The timecode string value or the amount of frames.
    :type tcValue: str or int
    :param tcRate: The timecode frame rate.
    :type tcRate: float or int or long or str or :class:`lite_media_core.rate.FrameRate`
    :return: The conformed frame rate.
    :rtype: tuple(str, :class:`lite_media_core.rate.FrameRate`)
    :raise TimecodeException: When the input parameters are incorrect.
    """
    # Check timecode input types.
    if not isinstance(tcValue, str) and not isinstance(tcValue, int):
        raise TimecodeException("Invalid timecode value %r, should be int or str." % tcValue)

    # Check timecode frame rate.
    if not isinstance(tcRate, (rate.FrameRate, rate.NonStandardFrameRate)):
        try:
            tcRate = rate.FrameRate.fromCustomRate(tcRate)
        except rate.FrameRateException as error:
            raise TimecodeException("Invalid frame rate for timecode: %s." % error) from error

    # Check timecode string value.
    if isinstance(tcValue, str) and not isValidTimecodeStr(tcValue, frameRate=tcRate):

        # Attempt to convert the timecode string from a milliseconds based formatting.
        try:
            tcValue = _conformMilliSecondTimecode(tcValue, tcRate)

        except ValueError as error:
            raise TimecodeException("Invalid timecode value %r, "
                "not a valid timecode str syntax." % tcValue) from error

    return tcValue, tcRate


def _conformMilliSecondTimecode(tcString, frameRate):
    """ Conform a 'HH:MM:SS.MSMS' timecode string to 'HH:MM:SS:FF'.

    :param str tcString: The timecode string to conform.
    :param frameRate: The timecode frame rate to use for conforming.
    :type frameRate: :class:`lite_media_core.rate.FrameRate`
    :return: The conformed timecode string value.
    :rtype: str
    """
    validTimeCode, milliSeconds = tcString.split(".")
    tc = TimeCode.fromSeconds(float("0.%s" % milliSeconds), frameRate)
    return validTimeCode + ":%02d" % tc.frames


def isValidTimecodeStr(tcString, frameRate=24.0):
    """ Check if a timecode string is valid according to a certain rate.

    :param str tcString: A timecode string to check.
    :param frameRate: An optional timecode frame rate to validate against.
    :type frameRate: float or int or long or str or :class:`lite_media_core.rate.FrameRate`
    :return: Is provided timecode valid ?
    :rtype: bool
    """
    try:

        # Note, tcLib handles milliseconds based timecode since 1.2.0,
        # but math logic seems wrong:
        # test = tcLib.Timecode(24.0, '00:00:00.08')  80 milliseconds ~ 2 frames
        # test.frs = '0.083'
        # so force internal computation.
        MILLISECS_REGEX = r"\d\d:\d\d:\d\d\.[\d]*"
        if re.match(MILLISECS_REGEX, tcString):
            raise ValueError("Milliseconds-based timecode string")

        # Default tcLib check.
        tcLib.Timecode(float(frameRate), start_timecode=tcString)
        return True

    except ValueError:
        return False
