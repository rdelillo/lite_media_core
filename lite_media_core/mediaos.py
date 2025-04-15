""" Mediaos module.
"""
import os

import lite_media_core.path_utils

import lite_media_core.media


def walk(top, topdown=True, onerror=None, followlinks=False):
    """ Overrides os.walk to return lite_media_core media objects.

    :param str top: root of a tree to walk.
    :param bool topdown: walk topdown (bottom-up otherwise
    :param object onerror: optional function called on OSError.
    :param bool followlinks: visit directories pointed to by symlinks.
    :return: (dirpath, dirnames, filenames)
    :rtype: tuple
    """
    for root, dirs, files in os.walk(top, topdown=topdown, onerror=onerror, followlinks=followlinks):

        fileAndMedias = []
        sequences = lite_media_core.path_utils.sequence.Sequence.getSequences(root)

        for sequence in sequences:
            for file in sequence:
                files.remove(os.path.basename(file))

        items = sequences + files

        for item in items:
            if isinstance(item, lite_media_core.path_utils.sequence.Sequence):
                path = item.format(lite_media_core.path_utils.sequence.PredefinedFormat.RV_EXTENDED)
            else:
                path = os.path.join(root, item)

            # Try to create a media object from file.
            try:
                fileAndMedias.append(lite_media_core.media.Media.fromPath(path))

            # Not a media, add into file list as a regular file.
            except lite_media_core.media.UnsupportedMimeType:
                fileAndMedias.append(os.path.basename(path))

        # Yield result for root directory.
        yield root, dirs, fileAndMedias


def identifyFromFiles(files):
    """ Identify medias from provided file paths.

    :param list files: list of file paths.
    :return: the list of medias.
    :rtype: list of :class:`lite_media_core.media.Media`
    """
    medias = []

    # Concatenate potential sequence(s) from provided files list.
    items = list(lite_media_core.path_utils.getSequences(files))

    # Identify potential medias from sequences.
    for item in items:

        if isinstance(item, lite_media_core.path_utils.Sequence):
            path = item.format(lite_media_core.path_utils.sequence.PredefinedFormat.RV_EXTENDED)
        else:
            path = str(item)

        try:
            medias.append(lite_media_core.media.Media.fromPath(path))

        except lite_media_core.media.UnsupportedMimeType:
            pass  # not a media, ignore.

    return medias
