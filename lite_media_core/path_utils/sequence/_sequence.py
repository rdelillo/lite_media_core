""" Sequence object.
"""

from __future__ import absolute_import

import os
import fnmatch
import glob

import fileseq

from lite_media_core.path_utils.sequence import _formats
from lite_media_core.path_utils.sequence import _frameRange
from lite_media_core.path_utils.sequence import _utils


class SequenceError(Exception):
    """ Base exception for sequence.
    """


class NoFrameRangeError(SequenceError):
    """ Raised when we try to access frame range information in a sequence with no frame range.
    """


class FrozenSequenceError(SequenceError):
    """ Raised when trying to modify an immutable Sequence.
    """


class Sequence:
    """ A Sequence object.
    """

    def __init__(self, fileSeqObj):
        """ Initialize a Sequence from a pySeq object.

        :param fileSeqObj: The reference pySeq object.
        :type fileSeqObj: :class:`fileseq.FileSequence`
        :raise ValueError: When the provided reference object is not a fileseq.FileSequence object
            or if the sequence object has no padding.
        """
        if not isinstance(fileSeqObj, (Sequence, fileseq.FileSequence)):
            raise ValueError("Cannot initialize a Sequence from %r." % fileSeqObj)

        # Allow a sequence to be created from frozen sequence and vice-versa
        if isinstance(fileSeqObj, Sequence):
            fileSeqObj = fileSeqObj._data

        # There are some FileSequence object we don't support (ex: single file without any frame info)
        try:
            _utils.validateFileSequence(fileSeqObj)
        except ValueError as error:
            raise ValueError("Cannot initialize a Sequence from %r: %s" % (fileSeqObj, error)) from error

        self._singleFrame = len(fileSeqObj.frameSet()) == 1

        self._data = fileSeqObj

    def __iter__(self):
        """
        :return: The path(s) of the Sequence.
        :rtype: Generator[str]
        """
        if not self.hasFrameRange:
            return

        for path in self._data:
            yield os.path.abspath(path)

    def __len__(self):
        """
        :return: The number of path(s) in the sequence.
        :rtype: int
        """
        return len(self._data)

    def __eq__(self, other):
        """
        :param other: Another sequence object
        :type other: :class:`Sequence`
        :return: True if both sequences are equal. False otherwise.
        :rtype: bool
        """
        return tuple(self) == tuple(other)

    def __ne__(self, other):
        """
        :param other: Another sequence object
        :type other: :class:`Sequence`
        :return: True if both sequences and different. False otherwise.
        :rtype: bool
        """
        return repr(self) != repr(other)

    def __hash__(self):
        """
        :return: A hashed representation of the sequence.
        :rtype: int
        """
        return hash(tuple(self))

    def __repr__(self):
        """
        :return: The representation of the Sequence.
        :rtype: str
        """
        return "<%s %r>" % (self.__class__.__name__, self._data)

    def __str__(self):
        """
        :return: The string representation of the Sequence.
        :rtype: str
        """
        return "<%s '%s'>" % (self.__class__.__name__, self.format(_formats.PredefinedFormat.NUKE_EXTENDED),)

    @property
    def end(self):
        """
        :return: The end frame of the Sequence.
        :rtype: str
        :raises NoFrameRangeError: If there's no frame range available
        """
        if not self.hasFrameRange:
            raise NoFrameRangeError("No frame range information available.")

        return os.path.abspath(self._data.frame(self._data.end()))

    @property
    def head(self):
        """
        :return: The Sequence head string (before the frame range).
        :rtype: str
        """
        return self._data.basename()

    @property
    def missing(self):
        """
        :return: A list of the missing frames.
        :rtype: list
        """
        return [
            self._data.frame(frame) for frame in fileseq.FrameSet(self._data.frameSet().invertedFrameRange())
        ]

    @property
    def padding(self):
        """
        :return: The maximum padding of the Sequence.
        :rtype: int
        """
        return max((self._data.zfill(), len(str(max(self._data.frameSet()))) if self.hasFrameRange else 1,))

    @property
    def hasFrameRange(self):
        """
        :return: Does the sequence have frame range information?
        :rtype: bool
        """
        return bool(self._data.frameSet())

    @property
    def hasLeadingZeros(self):
        """
        :return: Is the sequence numbered with leading zeroes.
        :rtype: bool
        """
        return self._data.zfill() > 1

    @property
    def start(self):
        """
        :return: The first frame of the Sequence.
        :rtype: str
        :raises NoFrameRangeError: If there's no frame range available
        """
        if not self.hasFrameRange:
            raise NoFrameRangeError("No frame range information available.")

        return os.path.abspath(self._data.frame(self._data.start()))

    @property
    def tail(self):
        """
        :return: The Sequence tail string (after the frame range).
        :rtype: str
        """
        return self._data.extension()

    @property
    def frameRange(self):
        """
        :return: The sequence frame range.
        :rtype: :class:`lite_media_core.path_utils.sequence.FrameRange`
        :raises NoFrameRangeError: If there's no frame range available
        """
        if not self.hasFrameRange:
            raise NoFrameRangeError("No frame range information available.")

        return _frameRange.FrameRange(
            self._data.start(),
            self._data.end(),
            padding=self.padding,
            missing=list(fileseq.FrameSet(self._data.frameSet().invertedFrameRange())),
        )

    def format(self, formatStr):
        """ Format the Sequence based on a format string.

        :param formatStr: The format string.
        :type formatStr: str or :class:`lite_media_core.path_utils.sequence.PredefinedFormat`
        :return: The formatted sequence.
        :rtype: str
        """
        if self._singleFrame:
            return self.start  # no need to format, there is only one path

        return _formats.formatSequence(self, formatStr)

    def getFramePath(self, frameNumber):
        """ Get the frame path from a provided frame number.

        :param int frameNumber: A provided frame number.
        :return: The frame file path.
        :rtype: str
        :raises ValueError: If the frame number is not part of the sequence.
        """
        # TO REVISIT: for now we consider explicit missing frames as 'invalid'.
        # An explicit missing frame means that the frame is purposefully not part
        # of the sequence, this might not be related to the the path existing on disk or not.
        if frameNumber not in self._data.frameSet():
            raise ValueError("Invalid frame number: %r." % frameNumber)

        return self._data.frame(frameNumber)

    @classmethod
    def fromString(cls, strData, allowEmpty=False):
        """ Initialize a Sequence object from a string.

        :param str strData: The data to initialize the Sequence from.
        :param bool allowEmpty: Allow the creation of a FrameRange with
        :return: The created Sequence object.
        :rtype: :class:`Sequence`
        :raise ValueError: When the provided string could not be uncompressed as a Sequence object.
        """
        fileSeqSequence = fileseq.FileSequence(_utils.conformPath(strData))

        # lite_media_core.path_utils-<1.1 did not support Sequence without a frame range
        # The allowEmpty flow is False by default for backward compatibility.
        if not allowEmpty and not fileSeqSequence.frameSet():
            raise ValueError("Path have no frame range information: %r" % strData)

        return cls(fileSeqSequence)

    @classmethod
    def discoverFromDisk(cls, strData):
        """ Analyse files on disk to match a sequence, extended (with framerange) or not.

        :param str strData: The data to initialize the Sequence from.
        :return: A list of created Sequence object.
        :rtype: list(:class:`Sequence`)
        """
        # Start by using glob to match unix patterns
        matches = glob.glob(strData)
        if matches:
            for sequence in cls.iterSequences(matches):
                yield sequence
            return

        # Do not consider deprecated formats
        formats = set(_formats.PredefinedFormat) - _formats.DEPRECATED_FORMATS

        # We will explore the sequences under the provided path directory and see it any match.
        # There can be multiple directory to explore if UNIX patterns are used. (ex: '/a/*/c/*.exr')
        directories = glob.iglob(os.path.dirname(strData) + os.sep)
        for directory in directories:
            for sequence in cls.iterSequences(directory):
                for formatStr in formats:
                    guess = sequence.format(formatStr)
                    if fnmatch.fnmatch(guess, strData):
                        yield sequence
                        break

                # Handle single-frame sequences.
                else:
                    if (
                        len(sequence) == 1
                        and strData.startswith(os.path.join(directory, sequence.head))
                        and strData.endswith(sequence.tail)
                    ):
                        yield sequence

    @classmethod
    def fromList(cls, listData, singleEntry=True):
        """ Initialize a Sequence object from a list.

        :param list listData: The data to initialize the Sequence from.
        :param bool singleEntry: Should we return one or multiple sequences? For backward compatibility.
        :return: A Sequence object or a list of Sequence objects.
        :rtype: :class:`Sequence` or list(:class:`Sequence`)
        :raises ValueError: If no sequence could be resolved.
        """
        fileSeqObjs = _utils.findSequencesInList(listData)[0]
        if fileSeqObjs:
            if singleEntry:
                return cls(fileSeqObjs[0])
            return [cls(fileSeqObj) for fileSeqObj in fileSeqObjs]
        raise ValueError("Could not find any sequence in %s" % listData)

    @classmethod
    def iterSequences(cls, data):
        """ Initialize Sequence objects(s) from a provided path.

        :param data: The directory/files path(s) to parse.
        :type data: str or list of str
        :return: A generator of Sequence objects found for the provided directory/files path(s).
        :rtype: Generator[:class:`Sequence`]
        """
        if isinstance(data, str):
            for fileSeqSequence in _utils.findSequencesOnDisk(data):
                yield cls(fileSeqSequence)
        else:
            for fileSeqSequence in _utils.findSequencesInList(data)[0]:
                yield cls(fileSeqSequence)

    @classmethod
    def getSequences(cls, data):
        """ Initialize Sequence object(s) from a provided data.

        :param data: The directory/files path(s) to parse.
        :type data: str or list of str
        :return: The Sequence objects found for the provided directory/files path(s).
        :rtype: list

        Sequence.getSequences('/path/to/a/directory/to/parse')
        Sequence.getSequences(['file.1.ext', 'file.2.ext', 'aa.ext'])
        """
        return list(cls.iterSequences(data))

    def addFrames(self, *frames):
        """ Add frames to the sequence

        :param frames: The frames to add
        :type frames: tuple
        """
        frameSet = self._data.frameSet()
        frames = set(_frameRange.FrameRange.fromData(frames))
        self._data.setFrameSet(frameSet | frames)

    def removeFrames(self, *frames):
        """ Remove frames from the sequence

        :param frames: The frames to add
        :type frames: tuple
        """
        frameSet = self._data.frameSet()
        frames = set(_frameRange.FrameRange.fromData(frames))
        self._data.setFrameRange(frameSet - frames)

    def setFrames(self, *frames):
        """ Set the sequence frames

        :param frames: The frames to set
        :type frames: tuple
        """
        frames = set(_frameRange.FrameRange.fromData(frames))
        self._data.setFrameRange(frames)

    def setPadding(self, padding):
        """ Change the sequence padding

        :param int padding: The new padding.
        """
        self._data.setPadding(fileseq.getPaddingChars(padding))


class FrozenSequence(Sequence):
    """ An immutable Sequence.
    """

    def addFrames(self, *frames):
        """ Add frames to the sequence

        :param frames: The frames to add
        :type frames: tuple
        :raises FrozenSequenceError: Always
        """
        raise FrozenSequenceError("Cannot modify a frozen sequence.")

    def removeFrames(self, *frames):
        """ Remove frames from the sequence

        :param frames: The frames to add
        :type frames: tuple
        :raises FrozenSequenceError: Always
        """
        raise FrozenSequenceError("Cannot modify a frozen sequence.")

    def setFrames(self, *frames):
        """ Set the sequence frames

        :param frames: The frames to set
        :type frames: tuple
        :raises FrozenSequenceError: Always
        """
        raise FrozenSequenceError("Cannot modify a frozen sequence.")

    def setPadding(self, padding):
        """ Change the sequence padding

        :param int padding: The new padding.
        :raises FrozenSequenceError: Always
        """
        raise FrozenSequenceError("Cannot modify a frozen sequence.")
