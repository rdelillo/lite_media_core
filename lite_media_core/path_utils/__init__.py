""" lite_media_core.path_utils module
"""
from typing import Union

from lite_media_core.path_utils.sequence import Sequence, _utils
from lite_media_core.path_utils.single_file import SingleFile

__all__ = ["SingleFile", "Sequence", "fromString", "getSequences"]


def from_string(str_data: str) -> Union[Sequence, SingleFile]:
    """ Initialize a SingleFile or a Sequence object from a string.
    """
    try:
        return Sequence.from_string(str_data)

    except ValueError:
        return SingleFile(str_data)


def get_sequences(data: Union[str, list]) -> list:
    """ Initialize SingleFile and Sequence object(s) from a provided data.

    get_sequences('/path/to/a/directory')
    get_sequences(['file.1.ext', 'file.2.ext', 'aa.ext'])
    """
    data = {data} if isinstance(data, str) else set(data)
    file_seq_objs, remains = _utils.find_sequences_in_list(data)

    for file_seq_obj in file_seq_objs:
        yield Sequence(file_seq_obj)

    for remain in remains:
        try:
            yield Sequence.from_string(remain)
        except ValueError:
            yield remain
