""" FrameRange object
"""

from __future__ import absolute_import

import itertools
import re

import six
import fileseq

_FRAMERANGE_GROUP_REGEX = re.compile(r"(?P<start>\-?\d+)\-(?P<end>\-?\d+)(?:x(?P<step>\d+))?")


class FrameRange:
    """ A FrameRange object.
    """

    def __init__(
        self, start, end, padding=None, missing=None, step=None
    ):  # pylint: disable=too-many-arguments
        """ Initialize a FrameRange object.

        :param int start: The frame range start digit.
        :param int end: The frame range end digit.
        :param int padding: An optional padding digit.
        :param list missing: An optional list of missing frames.
        :param int step: An optional frame range step.
        """
        self._start = start
        self._end = end
        self._step = step or 1
        self._missing = list(missing) if missing else []
        self._padding = padding or len(str(end))

    def __eq__(self, other):
        """
        :param object other: An object to compare
        :return: Whether self and other are equal.
        :rtype: bool
        """
        return repr(self) == repr(other)

    def __hash__(self):
        """
        :return: The hash of this FrameRange.
        :rtype: int
        """
        return hash(self.__repr__())

    def __repr__(self):
        """
        :return: The representation of the FrameRange.
        :rtype: str
        """
        return "<%s start=%s end=%s padding=%s step=%s missing=%s>" % (
            self.__class__.__name__,
            self._start,
            self._end,
            self._padding,
            self._step,
            self._missing,
        )

    def __str__(self):
        """
        :return: The string representation of the FrameRange's frames.
        :rtype: str
        """
        frameIterator = iter(self)
        latest = next(frameIterator)
        output = "%s" % latest

        for frame in frameIterator:
            output += ("-%s" if frame - latest == self.step else ", %s") % frame
            latest = frame

        # When building the string, stepped groups are added as "a-b-c-d-e".
        # For instance, "10-20-30-40-50". This regex strips the middle digits
        # to just keep "10-50". It adds a step pattern if step is not 1.
        return re.sub(r"(\d+)[-\d+]*(-\d+)", r"\1\2" + ("" if self.step == 1 else "x%s" % self.step), output)

    def __iter__(self):
        """ Iterable over the frames.

        :return: The frames of the FrameRange.
        :rtype: Generator[int]
        """
        frames = set(six.moves.xrange(self._start, self._end + self._step, self._step)) - set(self._missing)
        for frame in sorted(frames):
            yield frame

    def chunks(self, chunkSize):
        """ Yield successive chunkSize-sized tuples of frames.

        :param int chunkSize: Size of each chunk. Must be greater than 0.
        :return: An iterator that yield chunk of frames
        :rtype: Generator[tuple[int]]
        :raise ValueError: If chunkSize is less than 1.
        """
        if chunkSize < 1:
            raise ValueError("chunkSize must be greater than 0.")

        iterator = iter(self)
        chunk = tuple(itertools.islice(iterator, chunkSize))

        while chunk:
            yield chunk
            chunk = tuple(itertools.islice(iterator, chunkSize))

    def iterRanges(self):
        """ Yield sub-ranges.
        E.g. (10-14, 17-20) yields (10-14), (17-20)

        :return: An iterator that yield sub frame ranges.
        :rtype: Generator[:class:`FrameRange`]
        """
        if not self._missing:
            yield self

        else:
            allFrames = list(self)
            first = allFrames.pop(0)
            previous = first
            current = None
            for current in allFrames:
                if current - previous != self._step:
                    yield FrameRange(first, previous, padding=self._padding, step=self._step)
                    first = current

                previous = current

            yield FrameRange(first, current, padding=self._padding, step=self._step)

    @property
    def start(self):
        """
        :return: The start of the FrameRange.
        :rtype: int
        """
        return self._start

    @property
    def end(self):
        """
        :return: The end of the FrameRange.
        :rtype: int
        """
        return self._end

    @property
    def padding(self):
        """
        :return: The FrameRange padding.
        :rtype: int
        """
        return self._padding

    @property
    def step(self):
        """
        :return: The FrameRange step.
        :rtype: int
        """
        return self._step

    @property
    def missing(self):
        """
        :return: A list of missing frames.
        :rtype: list
        """
        return self._missing

    @classmethod
    def fromString(cls, strData):
        """ Initialize a FrameRange object from a string.

        :param str strData: The data to initialize the FrameRange from.
        :return: The created FrameRange object.
        :rtype: :class:`FrameRange`
        :raise ValueError: If strData is not a valid string,
               or if multiple different steps are provided in strData.
        """
        frames = set()
        steps = set()

        # Sanity check
        if not re.match(r"^-?\d[\d,-x ]*?", strData or ""):
            raise ValueError("Invalid input string: %r" % strData)

        for frameGroup in strData.split("," if "," in strData else " "):
            match = _FRAMERANGE_GROUP_REGEX.match(frameGroup.strip(" "))
            if match:
                frameStartStr, frameEndStr, frameSetStr = match.groups()
                if frameSetStr:
                    steps.add(int(frameSetStr))
                frames.update(range(int(frameStartStr), int(frameEndStr) + 1))
            else:
                frames.add(int(frameGroup))

        # Step management
        if len(steps) > 1:
            raise ValueError("Multiple steps detected in %r: %r" % (strData, sorted(steps)))
        if len(steps) == 1:
            step = steps.pop()
        else:
            step = 1

        # Discover missing frames
        start, end = min(frames), max(frames)
        missingFrames = set(range(start, end, step)) - frames
        return cls(start=start, end=end, step=step, missing=sorted(missingFrames))

    @classmethod
    def fromData(cls, *frames):
        """ Initialize a FrameRange object from some frame data.

        :param object frames: Frame values to conform
        :return: The created FrameRange object.
        :rtype: :class:`FrameRange`
        :raises ValueError: If the provided value is invalid
        """
        frames = _conformToFrames(frames)
        minFrame = min(frames)
        maxFrame = max(frames)
        missingFrames = list(set(range(minFrame, maxFrame + 1)) - frames)
        return cls(start=minFrame, end=maxFrame, missing=missingFrames)


def _conformToFrames(value):
    """ Conform some data to a list of frames.

    :param object value: Frame values to conform
    :return: A conformed set of frame
    :rtype: set[int]
    :raises ValueError: If the provided value is invalid
    """
    if isinstance(value, int):
        return {value}

    if isinstance(value, (six.text_type, six.binary_type)):
        return set(FrameRange.fromString(value))

    if isinstance(value, (FrameRange, fileseq.FrameSet)):
        return set(value)

    if isinstance(value, six.moves.collections_abc.Sequence):  # pylint: disable=no-member
        result = set()
        for val in value:
            result.update(_conformToFrames(val))
        return result

    raise ValueError("Unsupported frame format %s: %s" % (type(value).__name__, value))
