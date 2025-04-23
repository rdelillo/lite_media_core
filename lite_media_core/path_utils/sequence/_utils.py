""" Helper methods for fileseq path conforming.
"""
import re

import fileseq

# Regex for the padding notation
# Will match: '#', '###', '@', '@@', '%d', '%03d', '$F', '$F4', etc
REGEX_PADDING = r"#+|@+|%(?:\d+)?d|\$F(?:\d+)?"

# Regex for a frame range notation
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


def conform_path(path: str) -> tuple:
    """ Conform a path to it can be processed by `fileseq`.

    This will convert any EXTENDED notation to CONTAINED notation.
    ex: "img.%04d.exr 1-10" -> "img.1-10%04d.exr"

    :raises ValueError: If the provided path is not a valid sequence path.
    """
    match = re.match(REGEX_SEQUENCE_PATH, path)
    if not match:
        raise ValueError(f"Invalid path: {path}.")

    (head, contained_frame_range, padding, tail, extended_frame_range, missing_frame_range,) = match.groups()

    if contained_frame_range and extended_frame_range:
        raise ValueError("Path cannot have both a contained and an extended frame range: %r" % path)

    # Resolve frame-range
    if contained_frame_range:
        frame_range = _conform_frame_range(contained_frame_range)

    elif extended_frame_range:
        frameSet = fileseq.FrameSet(_conform_frame_range(extended_frame_range))
        if missing_frame_range:
            frameSet -= fileseq.FrameSet(_conform_frame_range(missing_frame_range))
        frame_range = str(frameSet)

    else:
        frame_range = ""

    # If the padding suggested by the frame range is higher than what the padding suggest,
    # replace the padding by the suggested frame range padding.
    # ex: "0001-0010@@" -> "0001-0010@@@@"
    frange_hint = _get_suggested_padding(frame_range) if frame_range else None
    padding_hint = fileseq.getPaddingNum(_conform_padding(padding)) if padding else 1
    padding_number = frange_hint if frange_hint and frange_hint > padding_hint else padding_hint
    padding = fileseq.getPaddingChars(padding_number)

    return (head or "") + frame_range + padding + tail


def _conform_frame_range(value: str) -> str:
    """ Conform a frame range string for `fileseq`.
    """
    # Remove any unneeded space
    # "1, 2" -> "1,2"
    value = value.replace(" ", "")

    # Standard notation is not needed for a single frame.
    # "1001-1001" -> "1001"
    match = re.match(r"^(-?\d+)-(-?\d+)$", value)
    if match:
        start_frame, end_frame = match.groups()
        if start_frame == end_frame:
            value = start_frame

    return value


def _get_suggested_padding(value) -> int:
    """ From a provided frame range, extract the the padding number.
    The padding will always be 1 if the first frame does not start with '0'.

    Note: What happen if there is an ambiguity ?
    Is "1001-1010" zero padded? current implementation says no !.
    """
    first_frame_str = re.match(r"(-?\d+)", value).group()
    return len(first_frame_str) if first_frame_str.lstrip("-").startswith("0") else 1


def _conform_padding(value: str) -> str:
    """ Conform a padding value so it is compatible with fileseq.
    """
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


def _conform_discovered_fileSeq(sequence: fileseq.FileSequence) -> fileseq.FileSequence:
    """ Conform a raw fileSeq sequences obtained from discovery methods like:

    - `fileseq.findSequenceOnDisk`
    - `fileseq.findSequencesOnDisk`
    - `fileseq.findSequenceInList`

    By default, fileseq will consider "1001-1010" to have a padding of 4.
    Assume zero padding if the frame range start with "0" explicitly.
    """
    if sequence.zfill() == len(str(sequence.start())):
        sequence.setPadding(fileseq.getPaddingChars(1))

    return sequence


def validate_file_sequence(file_seq_obj: fileseq.FileSequence):
    """ Validate a fileseq sequence object can be used to create a sequence object.

    :raises ValueError: If the fileseq sequence object is invalid
    """
    # If there's no frameSet, we are not dealing with a sequence but a single path.
    if file_seq_obj.frameSet() is None:
        raise ValueError("Sequence has got no frame information.")


def find_sequences_on_disk(data: str) -> list:
    """ Wrapper around `fileseq.findSequencesOnDisk`.
    """
    for fileSeq_sequence in sorted(fileseq.findSequencesOnDisk(data), key=repr):
        try:
            validate_file_sequence(fileSeq_sequence)
        except ValueError:
            continue

        yield _conform_discovered_fileSeq(fileSeqSequence)


def find_sequences_in_list(list_data: list) -> tuple:
    """ Wrapper around `fileseq.findSequencesInList`.

    There are two ways of creating sequences from a list:
    - lite_media_core.path_utils.get_sequences
    - lite_media_core.path_utils.sequence.Sequence.from_list

    Both will refer this common logic, however they don't act the same when encountering a list containing
    non-sequence (`getSequences` yield a :class:`SingleFile`, `Sequence.fromList` will ignore it).
    """
    sequences = []
    remains = set(list_data)

    for fileSeq_sequence in sorted(fileseq.findSequencesInList(list_data), key=repr):
        # Hack: fileseq can incorrectly recognize a "contained" notation without a padding identifier.
        # >>> fileseq.findSequencesInList(['0001-0010.ext'])
        # [<FileSequence: '0001-10@@@@@.ext'>]
        # A common symptom is that the head of the sequence end with
        # a number which is weird by itself.
        if next(reversed(fileSeq_sequence.basename()), "").isdigit():
            continue

        try:
            validate_file_sequence(fileSeq_sequence)
        except ValueError:
            continue

        sequences.append(_conform_discovered_fileSeq(fileSeq_sequence))

        # We iter the FileSequence instead of the Sequence since the Sequence will normalize paths.
        for path in fileSeq_sequence:
            remains.discard(path)

    # Start by yielding sequence from string representation
    return sequences, remains
