""" Sequence object.
"""
import os
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

        if isinstance(fileSeqObj, Sequence):
            fileSeqObj = fileSeqObj._data

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
        return "<%s '%s'>" % (self.__class__.__name__, self.format(_formats.PredefinedFormat.LEGACY_HASHTAG_EXTENDED),)

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
