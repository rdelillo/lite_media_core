""" FrameRange object
"""
from typing import Union

import collections.abc
import itertools
import re

import fileseq

_FRAMERANGE_GROUP_REGEX = re.compile(r"(?P<start>\-?\d+)\-(?P<end>\-?\d+)(?:x(?P<step>\d+))?")


class FrameRange:
    """ A FrameRange object.
    """

    def __init__(
        self,
        start: int,
        end: int,
        padding: Union[int] = None,
        missing: Union[list] = None,
        step: Union[int] = None
    ):  # pylint: disable=too-many-arguments
        """ Initialize a FrameRange object.
        """
        self._start = start
        self._end = end
        self._step = step or 1
        self._missing = list(missing) if missing else []
        self._padding = padding or len(str(end))

    def __eq__(self, other: object) -> bool:
        """ Is equal ?
        """
        return repr(self) == repr(other)

    def __hash__(self) -> int:
        """ The hash of this FrameRange.
        """
        return hash(self.__repr__())

    def __repr__(self) -> str:
        """ The representation of the FrameRange.
        """
        return "<%s start=%s end=%s padding=%s step=%s missing=%s>" % (
            self.__class__.__name__,
            self._start,
            self._end,
            self._padding,
            self._step,
            self._missing,
        )

    def __str__(self) -> str:
        """ The string representation of the FrameRange's frames.
        """
        frame_iterator = iter(self)
        latest = next(frame_iterator)
        output = "%s" % latest

        for frame in frame_iterator:
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
        frames = set(range(self._start, self._end + self._step, self._step)) - set(self._missing)
        for frame in sorted(frames):
            yield frame

    def chunks(self, chunk_size: int) -> list:
        """ Yield successive chunk_size-sized tuples of frames.

        :raise ValueError: If chunkSize is less than 1.
        """
        if not isinstance(chunk_size, int) or chunk_size < 1:
            raise ValueError(f"Chunk size {chunk_size} must be greater than 0.")

        iterator = iter(self)
        chunk = tuple(itertools.islice(iterator, chunk_size))

        while chunk:
            yield chunk
            chunk = tuple(itertools.islice(iterator, chunk_size))

    def iter_ranges(self) -> list:
        """ Yield sub-ranges.
        E.g. (10-14, 17-20) yields (10-14), (17-20)
        """
        if not self._missing:
            yield self

        else:
            all_frames = list(self)
            first = all_frames.pop(0)
            previous = first
            current = None
            for current in all_frames:
                if current - previous != self._step:
                    yield FrameRange(first, previous, padding=self._padding, step=self._step)
                    first = current

                previous = current

            yield FrameRange(first, current, padding=self._padding, step=self._step)

    @property
    def start(self) -> int:
        """ The start of the FrameRange.
        """
        return self._start

    @property
    def end(self) -> int:
        """ The end of the FrameRange.
        """
        return self._end

    @property
    def padding(self) -> int:
        """ The FrameRange padding.
        """
        return self._padding

    @property
    def step(self) -> int:
        """ The FrameRange step.
        """
        return self._step

    @property
    def missing(self) -> list:
        """ The list of missing frames.
        """
        return self._missing.copy()

    @classmethod
    def from_string(cls, str_data: str):
        """ Initialize a FrameRange object from a string.

        :raise ValueError: If strData is not a valid string,
               or if multiple different steps are provided in strData.
        """
        frames = set()
        steps = set()

        # Sanity check
        if not re.match(r"^-?\d[\d,-x ]*?", str_data or ""):
            raise ValueError(f"Invalid input string: {str_data}.")

        for frame_group in str_data.split("," if "," in str_data else " "):
            match = _FRAMERANGE_GROUP_REGEX.match(frame_group.strip(" "))
            if match:
                frame_start_str, frame_end_str, frame_set_str = match.groups()
                if frame_set_str:
                    steps.add(int(frame_set_str))
                frames.update(range(int(frame_start_str), int(frame_end_str) + 1))
            else:
                frames.add(int(frame_group))

        # Step management
        if len(steps) > 1:
            raise ValueError(f"Multiple steps detected in {str_data}: {sorted(steps)}.")
        if len(steps) == 1:
            step = steps.pop()
        else:
            step = 1

        # Discover missing frames
        start, end = min(frames), max(frames)
        missing_frames = set(range(start, end, step)) - frames
        return cls(start=start, end=end, step=step, missing=sorted(missing_frames))

    @classmethod
    def from_data(
        cls,
        *frames: Union[str, int, fileseq.FrameSet, collections.abc.Sequence]
    ):
        """ Initialize a FrameRange object from some frame data.

        :raises ValueError: If the provided value is invalid
        """
        frames = _conform_to_frames(frames)
        min_frame = min(frames)
        max_frame = max(frames)
        missing_frames = list(set(range(min_frame, max_frame + 1)) - frames)
        return cls(start=min_frame, end=max_frame, missing=missing_frames)


def _conform_to_frames(value: object) -> set:
    """ Conform some data to a list of frames.

    :raises ValueError: If the provided value is invalid
    """
    if isinstance(value, int):
        return {value}

    if isinstance(value, str):
        return set(FrameRange.from_string(value))

    if isinstance(value, (FrameRange, fileseq.FrameSet)):
        return set(value)

    if isinstance(value, collections.abc.Sequence):  # pylint: disable=no-member
        result = set()
        for val in value:
            result.update(_conform_to_frames(val))
        return result

    raise ValueError(f"Unsupported frame format {type(value).__name__}: {value}.")
