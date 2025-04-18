""" Sequence string formats.
"""
import enum


class PredefinedFormat(enum.Enum):
    """ Predefined string formats based on common applications and usage.
    """
    SPRINTF = 1
    LEGACY_HASHTAG = 2
    LEGACY_HASHTAG_EXTENDED = 3
    FFMPEG = 4

_EXTENDED_FORMATS = (
    PredefinedFormat.LEGACY_HASHTAG_EXTENDED,
)

PREDEFINED_FORMATS = {
    (PredefinedFormat.SPRINTF, False,): "{{dirname}}{{basename}}%d{{extension}}",  # files.%d.ext
    (PredefinedFormat.SPRINTF, True,): "{{dirname}}{{basename}}%{zfill:02}d{{extension}}",  # files.%04d.ext
    (PredefinedFormat.FFMPEG, False,): "{{dirname}}{{basename}}%d{{extension}}",  # files.%d.ext
    (PredefinedFormat.FFMPEG, True,): "{{dirname}}{{basename}}%{zfill:02}d{{extension}}",  # files.%04d.ext
    PredefinedFormat.LEGACY_HASHTAG: "{{dirname}}{{basename}}{null:#^{padding}}{{extension}}",  # files.####.ext
    PredefinedFormat.LEGACY_HASHTAG_EXTENDED: "{{dirname}}{{basename}}{null:#^{padding}}{{extension}} {frameRange}",  # files.####.ext 1-10
}


def formatSequence(sequence, predefinedFormat):
    """
    :param sequence: The sequence to format.
    :type sequence: :class:`lite_media_core.path_utils.sequence.Sequence`
    :param predefinedFormat: The predefined format to use for the string formatting.
    :type predefinedFormat: :class:`PredefinedFormat`
    :return: The formatted sequence as string.
    :rtype: str
    :raises ValueError: If the provided pyseq is incompatible with the format.
    """
    # We won't allow a sequence without any frame range to be formated to an extended format.
    if not sequence.hasFrameRange and predefinedFormat in _EXTENDED_FORMATS:
        raise ValueError("Could not format sequence without a frame range to an extended format.")

    # Resolve template to use
    try:
        template = PREDEFINED_FORMATS[predefinedFormat]
    except KeyError:
        try:
            template = PREDEFINED_FORMATS[(predefinedFormat, sequence.hasLeadingZeros)]
        except KeyError as error:
            raise ValueError("Unsupported format: %r" % predefinedFormat) from error

    pySeqSequence = sequence._data  # pylint: disable=protected-access
    sequencePadding = sequence.padding
    sequenceStart = pySeqSequence.start()
    sequenceEnd = pySeqSequence.end()

    return pySeqSequence.format(
        template.format(
            zfill=pySeqSequence.zfill(),
            padding=sequence.padding,
            frameRange="%s-%s" % (sequenceStart, sequenceEnd),
            start=str(sequenceStart),
            startPadded=str(sequenceStart).zfill(sequencePadding),
            end=str(sequenceEnd),
            endPadded=str(sequenceEnd).zfill(sequencePadding),
            null="",
        )
    )
