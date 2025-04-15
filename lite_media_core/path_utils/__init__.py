""" lite_media_core.path_utils module
"""

from __future__ import absolute_import

import six


from lite_media_core.path_utils.sequence import Sequence, _utils
from lite_media_core.path_utils.singleFile import SingleFile

__all__ = ["SingleFile", "Sequence", "fromString", "getSequences"]


def fromString(strData):
    """ Initialize a SingleFile or a Sequence object from a string.

    :param str strData: The data to initialize the object from.
    :return: The created object.
    :rtype: :class:`Sequence` or :class:`SingleFile`
    """
    try:
        return Sequence.fromString(strData)

    except ValueError:
        return SingleFile(strData)


def getSequences(data):
    """ Initialize SingleFile and Sequence object(s) from a provided data.

    :param data: The directory/files path(s) to parse.
    :type data: str or list of str
    :return: The SingleFile and Sequence objects found for the provided directory/files path(s).
    :rtype: list of :class:`Sequence` or :class:`SingleFile`

    getSequences('/path/to/a/directory/to/parse')
    getSequences(['file.1.ext', 'file.2.ext', 'aa.ext'])
    """
    data = {data} if isinstance(data, six.string_types) else set(data)
    fileSeqObjs, remains = _utils.findSequencesInList(data)

    for fileSeqObj in fileSeqObjs:
        yield Sequence(fileSeqObj)

    for remain in remains:
        try:
            yield Sequence.fromString(remain)
        except ValueError:
            yield remain
