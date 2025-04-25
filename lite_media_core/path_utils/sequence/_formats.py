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


def format_sequence(sequence: object, predefined_format: PredefinedFormat) -> str:
    """
    :raises ValueError: If the provided pyseq is incompatible with the format.
    """
    # Do not allow a sequence without any frame range to be formated to an extended format.
    if not sequence.has_frame_range and predefined_format in _EXTENDED_FORMATS:
        raise ValueError(f"Cannot format sequence without a frame range to {predefined_format}.")

    # Resolve template to use
    try:
        template = PREDEFINED_FORMATS[predefined_format]
    except KeyError:
        try:
            template = PREDEFINED_FORMATS[(predefined_format, sequence.has_leading_zeros)]
        except KeyError as error:
            raise ValueError(f"Unsupported format: {predefined_format}.") from error

    file_seq_sequence = sequence._data  # pylint: disable=protected-access
    sequence_padding = sequence.padding
    sequence_start = file_seq_sequence.start()
    sequence_end = file_seq_sequence.end()

    return file_seq_sequence.format(
        template.format(
            zfill=file_seq_sequence.zfill(),
            padding=sequence_padding,
            frameRange="%s-%s" % (sequence_start, sequence_end),
            start=str(sequence_start),
            startPadded=str(sequence_start).zfill(sequence_padding),
            end=str(sequence_end),
            endPadded=str(sequence_end).zfill(sequence_padding),
            null="",
        )
    )
