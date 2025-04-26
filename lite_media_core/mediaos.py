""" Mediaos module.
"""
import os

from lite_media_core import media
from lite_media_core import path_utils


def walk(top, topdown: bool = True, onerror: bool = None, followlinks: bool = False) -> tuple:
    """ Overrides os.walk to return media objects.
    """
    for root, dirs, files in os.walk(top, topdown=topdown, onerror=onerror, followlinks=followlinks):

        file_and_medias = []
        sequences = path_utils.sequence.Sequence.get_sequences(root)

        for sequence in sequences:
            for file in sequence:
                files.remove(os.path.basename(file))

        items = sequences + files

        for item in items:
            if isinstance(item, path_utils.sequence.Sequence):
                path = item.format(path_utils.sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED)
            else:
                path = os.path.join(root, item)

            # Try to create a media object from file.
            try:
                file_and_medias.append(media.Media.from_path(path))

            # Not a media, add into file list as a regular file.
            except media.UnsupportedMimeType:
                file_and_medias.append(os.path.basename(path))

        # Yield result for root directory.
        yield root, dirs, file_and_medias


def identify_from_files(files: list) -> list:
    """ Identify medias from provided file paths list.
    """
    medias = []

    # Concatenate potential sequence(s) from provided files list.
    items = list(path_utils.get_sequences(files))

    # Identify potential medias from sequences.
    for item in items:

        if isinstance(item, path_utils.Sequence):
            path = item.format(path_utils.sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED)
        else:
            path = str(item)

        try:
            medias.append(media.Media.from_path(path))

        except media.UnsupportedMimeType:
            pass  # not a media, ignore.

    return medias


def listdir(path: str) -> list:
    """ List a directory and identify media objects inside.
    """
    file_and_medias = []
    items = []

    if not os.path.isdir(path):
        raise ValueError(f"Provided path is not a directory: {path}")

    # List all entries in the directory
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        items.append(full_path)

    # Detect sequences first
    sequences = path_utils.sequence.Sequence.get_sequences(path)

    for sequence in sequences:
        for file in sequence:
            base = os.path.basename(file)
            full = os.path.join(path, base)
            if full in items:
                items.remove(full)

    # Merge sequences and remaining files
    items = sequences + items

    for item in items:
        if isinstance(item, path_utils.sequence.Sequence):
            media_path = item.format(path_utils.sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED)
        else:
            media_path = str(item)

        try:
            file_and_medias.append(media.Media.from_path(media_path))

        except media.UnsupportedMimeType:
            file_and_medias.append(os.path.basename(media_path))

    return file_and_medias
