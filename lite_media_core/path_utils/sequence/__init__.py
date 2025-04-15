""" Sequence module.
"""

from __future__ import absolute_import

from lite_media_core.path_utils.sequence._formats import PredefinedFormat
from lite_media_core.path_utils.sequence._frameRange import FrameRange
from lite_media_core.path_utils.sequence._sequence import (
    Sequence,
    SequenceError,
    FrozenSequence,
    NoFrameRangeError,
    FrozenSequenceError,
)


__all__ = [
    "FrameRange",
    "PredefinedFormat",
    "Sequence",
    "FrozenSequence",
    "SequenceError",
    "NoFrameRangeError",
    "FrozenSequenceError",
]
