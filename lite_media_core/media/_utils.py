""" Media utilities module.
"""
import itertools

from lite_media_core.path_utils import sequence as _sequence

from lite_media_core.media import _media


def chunkImageSequence(imageSequence, chunkSize):
    """ Helper, chunk a provided image sequence into a list of smaller image sequence(s).

    :param imageSequence: A image sequence to chunk.
    :type imageSequence: :class:`lite_media_core.media.ImageSequence`
    :param int chunkSize: The chunk size.
    :return: A list of the sub image sequences.
    :rtype: list of :class:`lite_media_core.media.ImageSequence`
    """
    chunkSequences = []
    chunkImages = itertools.zip_longest(*[iter(imageSequence)] * chunkSize)

    for chunk in chunkImages:
        chunk = [chunkBit.path for chunkBit in chunk if chunkBit]

        if len(chunk) == 1:
            mediaPath, = chunk
        else:
            sequence = _sequence.Sequence.fromList(list(chunk))
            mediaPath = sequence.format(_sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED)

        chunkSequences.append(_media.Media.fromPath(mediaPath))

    return chunkSequences
