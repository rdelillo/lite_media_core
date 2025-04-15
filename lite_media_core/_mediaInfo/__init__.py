""" mediaInfo module.
"""
import os

from lite_media_core._mediaInfo._base import MediaInfoException
from lite_media_core._mediaInfo import _mediaInfoAPI


def getMediaInformation(mediaFile):
    """ Get information from a media.

    :param str mediaFile: The input media file path.
    :return: The media information, metadata.
    :rtype: tuple (dict, :class:`collections.OrderedDict`)
    :raise ValueError: When the provided media is not supported.
    """
    if not os.path.exists(mediaFile):
        raise ValueError("Provided media does not exists: %r." % mediaFile)

    # Rely on Media Info to gather information.
    try:
        return _mediaInfoAPI.MediaInfoAPI.getMediaInformation(mediaFile)

    except MediaInfoException as error:
        raise ValueError("Unsupported provided media: %r." % mediaFile) from error
