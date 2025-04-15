""" path utilities.
"""

from __future__ import absolute_import

import os
import platform

from lite_media_core.path_utils.mimeTypes import mimetypes


_PLATFORM_CURRENT = platform.system()


def splitext(path, allowUnknownType=True):
    """ Split the pathname into a pair (root, ext) such that root + ext == path.
    Use known mime-types to detect ext.
    >>> os.path.splitext('/path/to/a/file.bgeo.sc')
    ('/path/to/a/file.bgeo', '.sc')
    >>> lite_media_core.path_utils.path.splitext('/path/to/a/file.bgeo.sc')
    ('/path/to/a/file', '.bgeo.sc')

    :param str path: The pathname to split.
    :param bool allowUnknownType: Shall this function continue when the provided extension is unknown.
    :return: The pathname split into a pair (root, ext) such that root + ext == path
    :rtype: tuple(str, str)
    :raise ValueError: When the provided path mime-type is unknown and unknown types are not allowed.
    """
    potential_types = []
    for ext in mimetypes.types_map:  # mimtypes.guess_extension does not support double extensions.
        if path.endswith(ext):
            potential_types.append(ext)

    if potential_types:
        ext = max(potential_types, key=len)
        return path[: -len(ext)], ext

    if allowUnknownType:
        return os.path.splitext(path)

    raise ValueError("Unknown mime-type for %r." % path)
