""" Sequence object.
"""
from typing import Union

import os
import fileseq

from lite_media_core.path_utils.sequence import _formats
from lite_media_core.path_utils.sequence import _frame_range
from lite_media_core.path_utils.sequence import _utils


class SequenceError(Exception):
    """ Base exception for sequence.
    """


class NoFrameRangeError(SequenceError):
    """ Raised when we try to access frame range information in a sequence with no frame range.
    """


class Sequence:
    """ A Sequence object.
    """

    def __init__(self, file_seq_obj: Union[fileseq.FileSequence]):
        """ Initialize a Sequence from a fileSeq object.

        :raise ValueError: When the provided reference object is not a fileseq.FileSequence object
            or if the sequence object has no padding.
        """
        if not isinstance(file_seq_obj, (Sequence, fileseq.FileSequence)):
            raise ValueError("Cannot initialize a Sequence from %r." % file_seq_obj)

        if isinstance(file_seq_obj, Sequence):
            file_seq_obj = file_seq_obj._data

        try:
            _utils.validate_file_sequence(file_seq_obj)

        except ValueError as error:
            raise ValueError("Cannot initialize a Sequence from %r: %s" % (file_seq_obj, error)) from error

        self._single_frame = len(file_seq_obj.frameSet()) == 1
        self._data = file_seq_obj

    def __iter__(self) -> list:
        """ Iterate over the path(s) of the Sequence.
        """
        if not self.has_frame_range:
            return

        for path in self._data:
            yield os.path.abspath(path)

    def __len__(self) -> int:
        """ The amount of path(s) in the sequence.
        """
        return len(self._data)

    def __eq__(self, other: object) -> bool:
        """ Is equal ?
        """
        return tuple(self) == tuple(other)

    def __ne__(self, other: object)  -> bool:
        """ Is not equal ?
        """
        return repr(self) != repr(other)

    def __hash__(self) -> int:
        """ Hash representation of the sequence.
        """
        return hash(tuple(self))

    def __repr__(self) -> str:
        """ The representation of the Sequence.
        """
        return f"<{self.__class__.__name__} {self._data}>"

    def __str__(self) -> str:
        """ The string representation of the Sequence.
        """
        return (
            f"<{self.__class__.__name__} "
            f"'{self.format(_formats.PredefinedFormat.LEGACY_HASHTAG_EXTENDED)}'>"
        )

    @property
    def end(self) -> str:
        """ The path to the end frame of the Sequence.

        :raises NoFrameRangeError: If there's no frame range available
        """
        if not self.has_frame_range:
            raise NoFrameRangeError("No frame range information available.")

        return os.path.abspath(self._data.frame(self._data.end()))

    @property
    def head(self) -> str:
        """ The Sequence head string (before the frame range).
        """
        return self._data.basename()

    @property
    def missing(self) -> list:
        """ A list of the missing frames.
        """
        return [
            self._data.frame(frame) for frame in fileseq.FrameSet(self._data.frameSet().invertedFrameRange())
        ]

    @property
    def padding(self) -> int:
        """ The maximum padding of the Sequence.
        """
        return max((self._data.zfill(), len(str(max(self._data.frameSet()))) if self.has_frame_range else 1,))

    @property
    def has_frame_range(self) -> bool:
        """ Does the sequence have frame range information?
        """
        return bool(self._data.frameSet())

    @property
    def has_leading_zeros(self) -> bool:
        """ Is the sequence numbered with leading zeroes ?
        """
        return self._data.zfill() > 1

    @property
    def start(self) -> str:
        """ The path to the first frame of the Sequence.
        
        :raises NoFrameRangeError: If there's no frame range available
        """
        if not self.has_frame_range:
            raise NoFrameRangeError("No frame range information available.")

        return os.path.abspath(self._data.frame(self._data.start()))

    @property
    def tail(self) -> str:
        """ The Sequence tail string (after the frame range).
        """
        return self._data.extension()

    @property
    def frame_range(self) -> _frame_range.FrameRange:
        """ The sequence frame range.

        :raises NoFrameRangeError: If there's no frame range available
        """
        if not self.has_frame_range:
            raise NoFrameRangeError("No frame range information available.")

        return _frame_range.FrameRange(
            self._data.start(),
            self._data.end(),
            padding=self.padding,
            missing=list(fileseq.FrameSet(self._data.frameSet().invertedFrameRange())),
        )

    def format(self, format_str: Union[str, _formats.PredefinedFormat]) -> str:
        """ Format the Sequence based on a format string.
        """
        if self._single_frame:
            return self.start  # no need to format, there is only one path

        return _formats.format_sequence(self, format_str)

    def get_frame_path(self, frame_number: int) -> str:
        """ Get the frame path from a provided frame number.

        :param int frameNumber: A provided frame number.
        :return: The frame file path.
        :rtype: str
        :raises ValueError: If the frame number is not part of the sequence.
        """
        if frame_number not in self._data.frameSet():
            raise ValueError(f"Invalid frame number: {frame_number}.")

        return self._data.frame(frame_number)

    @classmethod
    def from_string(cls, str_data: str, allow_empty: bool = False):
        """ Initialize a Sequence object from a string.

        :raise ValueError: When the provided string could not be uncompressed as a Sequence object.
        """
        file_seq_sequence = fileseq.FileSequence(_utils.conform_path(str_data))

        if not allow_empty and not file_seq_sequence.frameSet():
            raise ValueError(f"Path have no frame range information: {str_data}.")

        return cls(file_seq_sequence)

    @classmethod
    def from_list(cls, list_data: list, single_entry: bool = True):
        """ Initialize a Sequence object from a list.

        :raises ValueError: If no sequence could be resolved.
        """
        file_seq_objs = _utils.find_sequences_in_list(list_data)[0]

        if file_seq_objs:
            if single_entry:
                return cls(file_seq_objs[0])

            return [cls(file_seq_obj) for file_seq_obj in file_seq_objs]

        raise ValueError(f"Could not find any sequence in {list_data}.")

    @classmethod
    def iter_sequences(cls, data: Union[str, list]) -> list:
        """ Iterate over the Sequence objects(s) from a provided data.
            (path on disk or random list)
        """
        if isinstance(data, str):
            for file_seq_sequence in _utils.find_sequences_on_disk(data):
                yield cls(file_seq_sequence)
        else:
            for file_seq_sequence in _utils.find_sequences_in_list(data)[0]:
                yield cls(file_seq_sequence)

    @classmethod
    def get_sequences(cls, data: Union[str, list]) -> list:
        """ Initialize Sequence object(s) from a provided data.

        Sequence.get_sequences('/path/to/a/directory/to/parse')
        Sequence.get_sequences(['file.1.ext', 'file.2.ext', 'aa.ext'])
        """
        return list(cls.iterSequences(data))
