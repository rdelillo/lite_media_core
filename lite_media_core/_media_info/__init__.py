""" media_info module.
"""
import os

from lite_media_core._media_info._base import MediaInfoException
from lite_media_core._media_info import _media_info_api


def get_media_information(media_path: str) -> tuple:
    """ Get information from a media path.

    :raise ValueError: When the provided media is not supported.
    """
    if not os.path.exists(media_path):
        raise ValueError(f"Provided media does not exists: {media_path}.")

    # Rely on Media Info to gather information.
    try:
        return _media_info_api.MediaInfoAPI.get_media_information(media_path)

    except MediaInfoException as error:
        raise ValueError(f"Unsupported provided media: {media_path}.") from error
