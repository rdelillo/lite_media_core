""" Helper methods for fileseq path conforming.
"""

from __future__ import absolute_import

import re

import fileseq

# Regex for the padding notation we support
# Will match: '#', '###', '@', '@@', '%d', '%03d', '$F', '$F4', etc
REGEX_PADDING = r"#+|@+|%(?:\d+)?d|\$F(?:\d+)?"

# Regex for a frame range notation we support
# Will match: '1-2' '1,2' '1, 2' '1-2, 3' '1-2,3' '1,2-3'
REGEX_FRAME_RANGE = r"-?\d+(?:[-,(?:, )]+-?\d+)*"

# Regex that split a path into it's individual components
REGEX_SEQUENCE_PATH = (
    r"{head}?\(?{containedFrameRange}?\)?{padding}?{tail}"
    r"(?: {extendedFrameRange}(?: {missingFrames})?)?$".format(
        head=r"(?P<head>.*[_|./\\])",
        containedFrameRange=r"(?P<containedFrameRange>{0})".format(REGEX_FRAME_RANGE),
        padding=r"(?P<padding>{0})".format(REGEX_PADDING),
        tail=r"(?P<tail>(?:\.\w+)+)",
        extendedFrameRange=r"\[*(?P<extendedFrameRange>{0})\]*".format(REGEX_FRAME_RANGE),
        missingFrames=r"\(?\[*(?P<missingFrameRange>{0})\]*\)?".format(REGEX_FRAME_RANGE),
    )
)


def conformPath(path):
    """ Conform a path to it can be processed by `fileseq`.

    This will convert any EXTENDED notation to CONTAINED notation.
    ex: "img.%04d.exr 1-10" -> "img.1-10%04d.exr"

    :param str path: A path string
    :return: The path, it's extended frame range if any and it's missing frame range if any.
    :rtype: tuple(str, str or None, str or None)
    :raises ValueError: If the provided path is not a valid sequence path.
    """
    match = re.match(REGEX_SEQUENCE_PATH, path)
    if not match:
        raise ValueError("Invalid path: %r" % path)

    (head, containedFrameRange, padding, tail, extendedFrameRange, missingFrameRange,) = match.groups()

    if containedFrameRange and extendedFrameRange:
        raise ValueError("Path cannot have both a contained and an extended frame range: %r" % path)

    # Resolve frame-range
    if containedFrameRange:
        frameRange = _conformFrameRange(containedFrameRange)
    elif extendedFrameRange:
        frameSet = fileseq.FrameSet(_conformFrameRange(extendedFrameRange))
        if missingFrameRange:
            frameSet -= fileseq.FrameSet(_conformFrameRange(missingFrameRange))
        frameRange = str(frameSet)
    else:
        frameRange = ""

    # Resolve padding
    # If the padding suggested by the frame range is higher than what the padding suggest,
    # replace the padding by the suggested frame range padding.
    # ex: "0001-0010@@" -> "0001-0010@@@@"
    frangeHint = _getFrameRangeSuggestedPadding(frameRange) if frameRange else None
    paddingHint = fileseq.getPaddingNum(_conformPadding(padding)) if padding else 1
    paddingNumber = frangeHint if frangeHint and frangeHint > paddingHint else paddingHint
    padding = fileseq.getPaddingChars(paddingNumber)

    return (head or "") + frameRange + padding + tail


def _conformFrameRange(value):
    """ Conform a frame range string for `fileseq`.

    :param str value: A frame range string
    :return: A frame range conformed for fileseq
    :rtype: str
    """
    # Remove any unneeded space
    # "1, 2" -> "1,2"
    value = value.replace(" ", "")

    # Standard notation is not needed for a single frame.
    # "1001-1001" -> "1001"
    match = re.match(r"^(-?\d+)-(-?\d+)$", value)
    if match:
        startFrame, endFrame = match.groups()
        if startFrame == endFrame:
            value = startFrame

    return value


def _getFrameRangeSuggestedPadding(value):
    """ From a provided frame range, extract the the padding number.
    The padding will always be 1 if the first frame does not start with '0'.

    Note: This logic control what happen if there's ambiguity.
    Is "1001-1010" zero padded? lite_media_core.path_utils current implementation say no.

    :param str value: A frame range string
    :return: The suggested padding number
    :rtype: int
    """
    firstFrameStr = re.match(r"(-?\d+)", value).group()
    return len(firstFrameStr) if firstFrameStr.lstrip("-").startswith("0") else 1


def _conformPadding(value):
    """ Conform a padding value so it is compatible with fileseq.

    :param str value: A padding string (ex: '%04d')
    :return: A conformed padding string
    :rtype: str
    """
    # Houdini edge-case
    if value.startswith("$F"):
        padding = value.lstrip("$F")
        return "@" * int(padding) if padding else "@"

    for src, dst in (
        ("#", "@"),  # 'img.###.exr' -> 'img.@@@.exr'
        ("%0d", "%1d"),  # 'img.%0d.exr' -> 'img.%01d.exr'
        ("%d", "%1d"),  # 'img.%d.exr' -> 'img.%1d.exr'
    ):
        value = value.replace(src, dst)

    return value


def _conformDiscoveredFileSeq(sequence):
    """ Conform a raw fileSeq sequence object obtained from discovery methods like:

    - `fileseq.findSequenceOnDisk`
    - `fileseq.findSequencesOnDisk`
    - `fileseq.findSequenceInList`

    By default, fileseq will consider "1001-1010" to have a padding of 4.
    We only assume zero padding if the frame range start with "0" explicitly.

    :param sequence: A fileseq sequence object
    :type sequence: :class:`fileseq.FileSequence`
    :return: A conformed fileseq sequence object
    :rtype: :class:`fileseq.FileSequence`
    """
    if sequence.zfill() == len(str(sequence.start())):
        sequence.setPadding(fileseq.getPaddingChars(1))

    return sequence


def validateFileSequence(fileSeqObj):
    """ Validate a fileseq sequence object can be used to create a sequence object.

    :param fileSeqObj: A fileseq sequence object
    :type fileSeqObj: :class:`fileseq.FileSequence`
    :raises ValueError: If the fileseq sequence object is invalid
    """
    # If there's no frameSet, we are not dealing with a sequence but a single path.
    if fileSeqObj.frameSet() is None:
        raise ValueError("Sequence have no frame information.")


def findSequencesOnDisk(data):
    """ Wrapper around `fileseq.findSequencesOnDisk`.

    :param str data: A location on disk to scan
    :return: A list of fileseq FileSequence object.
    :rtype: list(:class:`fileseq.FileSequence`)
    """
    for fileSeqSequence in sorted(fileseq.findSequencesOnDisk(data), key=repr):
        try:
            validateFileSequence(fileSeqSequence)
        except ValueError:
            continue

        yield _conformDiscoveredFileSeq(fileSeqSequence)


def findSequencesInList(listData):
    """ Wrapper around `fileseq.findSequencesInList`.

    There are two ways of creating sequences from a list:
    - lite_media_core.path_utils.getSequences
    - lite_media_core.path_utils.sequence.Sequence.fromList

    Both will refer this common logic, however they don't act the same when encountering a list containing
    non-sequence (`getSequences` yield a :class:`SingleFile`, `Sequence.fromList` will ignore it).

    :param list listData: The data to initialize the Sequence from.
    :return: A list of fileseq FileSequence objects and a list of values that where not recognised.
    :rtype: tuple(list(:class:`fileseq.FileSequence`), set(str))
    """
    sequences = []
    remains = set(listData)

    for fileSeqSequence in sorted(fileseq.findSequencesInList(listData), key=repr):
        # Hack: fileseq can incorrectly recognize a "contained" notation without a padding identifier.
        # >>> fileseq.findSequencesInList(['0001-0010.ext'])
        # [<FileSequence: '0001-10@@@@@.ext'>]
        # A common symptom is that the head of the sequence end with
        # a number which is weird by itself.
        if next(reversed(fileSeqSequence.basename()), "").isdigit():
            continue

        try:
            validateFileSequence(fileSeqSequence)
        except ValueError:
            continue

        sequences.append(_conformDiscoveredFileSeq(fileSeqSequence))

        # We iter the FileSequence instead of the Sequence since the Sequence will normalize paths.
        for path in fileSeqSequence:
            remains.discard(path)

    # Start by yielding sequence from string representation
    return sequences, remains
