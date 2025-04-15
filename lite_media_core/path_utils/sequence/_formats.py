""" Sequence string formats.
"""

from __future__ import absolute_import

import warnings

import enum


class PredefinedFormat(enum.Enum):
    """ Predefined string formats based on common applications and usage.
    """

    HOUDINI = 1
    HOUDINI_ALTERNATIVE = 7  # deprecated in favor of HOUDINI
    NUKE = 2
    NUKE_EXTENDED = 3
    RV = 4
    RV_EXTENDED = 5
    SPRINTF = 6
    LEGACY_HASHTAG = 8
    LEGACY_HASHTAG_EXTENDED = 9
    FFMPEG = 10
    KATANA = 11


DEPRECATED_FORMATS = {
    PredefinedFormat.HOUDINI_ALTERNATIVE,
}

_EXTENDED_FORMATS = (
    PredefinedFormat.NUKE_EXTENDED,
    PredefinedFormat.RV_EXTENDED,
    PredefinedFormat.LEGACY_HASHTAG_EXTENDED,
)

PREDEFINED_FORMATS = {
    (PredefinedFormat.HOUDINI, False,): "{{dirname}}{{basename}}$F{{extension}}",  # ex: files.$F.ext
    (PredefinedFormat.HOUDINI, True,): "{{dirname}}{{basename}}$F{zfill}{{extension}}",  # files.$F4.ext
    (PredefinedFormat.NUKE, False,): "{{dirname}}{{basename}}%d{{extension}}",  # files.%d.ext
    (PredefinedFormat.NUKE, True,): "{{dirname}}{{basename}}%{zfill:02}d{{extension}}",  # files.%04d.ext
    (
        PredefinedFormat.NUKE_EXTENDED,
        False,
    ): "{{dirname}}{{basename}}%d{{extension}} {frameRange}",  # files.%d.ext 1-10
    (
        PredefinedFormat.NUKE_EXTENDED,
        True,
    ): "{{dirname}}{{basename}}%{zfill:02}d{{extension}} {frameRange}",  # files.%04d.ext 1-10
    (PredefinedFormat.SPRINTF, False,): "{{dirname}}{{basename}}%d{{extension}}",  # files.%d.ext
    (PredefinedFormat.SPRINTF, True,): "{{dirname}}{{basename}}%{zfill:02}d{{extension}}",  # files.%04d.ext
    (PredefinedFormat.FFMPEG, False,): "{{dirname}}{{basename}}%d{{extension}}",  # files.%d.ext
    (PredefinedFormat.FFMPEG, True,): "{{dirname}}{{basename}}%{zfill:02}d{{extension}}",  # files.%04d.ext
    PredefinedFormat.LEGACY_HASHTAG: "{{dirname}}{{basename}}{null:#^{padding}}{{extension}}",  # files.####.ext
    PredefinedFormat.LEGACY_HASHTAG_EXTENDED: "{{dirname}}{{basename}}{null:#^{padding}}{{extension}} {frameRange}",  # files.####.ext 1-10
    PredefinedFormat.RV: "{{dirname}}{{basename}}{rvPadding}{{extension}}",  # files.@@@.exr
    PredefinedFormat.RV_EXTENDED: "{{dirname}}{{basename}}{startPadded}-{endPadded}{rvPadding}{{extension}}",  # files.1-10@@@.exr
    PredefinedFormat.KATANA: "{{dirname}}{{basename}}({start}-{end})%{zfill:02}d{{extension}}",  # files.(1-10)%04d.exr
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

    # HOUDINI_ALTERNATIVE is deprecated, raise a warning if it's used.
    if predefinedFormat == PredefinedFormat.HOUDINI_ALTERNATIVE:
        warnings.warn(
            "HOUDINI_ALTERNATIVE is deprecated, please use HOUDINI instead.", DeprecationWarning,
        )
        predefinedFormat = PredefinedFormat.HOUDINI

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
            rvPadding="#" if sequence.padding == 4 else "@" * sequencePadding,
            start=str(sequenceStart),
            startPadded=str(sequenceStart).zfill(sequencePadding),
            end=str(sequenceEnd),
            endPadded=str(sequenceEnd).zfill(sequencePadding),
            null="",
        )
    )
