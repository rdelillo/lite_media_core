""" MediaInfo based media info inspector.
"""
import collections
import os
import ctypes
import sys


def  __get_library_paths(os_is_nt):
    """ Need to hack pymediainfo.MediaInfo in order to redirect to current local lib.
    """
    script_dir = os.path.dirname(__file__)
    resource_dir = os.path.join(script_dir, "dll_resources")

    if os_is_nt:
        library_paths = ("MediaInfo.dll",)
    elif sys.platform == "darwin":
        library_paths = ("libmediainfo.0.dylib", "libmediainfo.dylib")
    else:
        for additional_lib in ("libtinyxml2.so.6", "libmms.so.0", "libzen.so.0"):
            ctypes.CDLL(os.path.join(resource_dir, additional_lib))

        library_paths = ("libmediainfo.so.0",)

    # Look for the library file in the script folder
    for library in library_paths:
        absolute_library_path = os.path.join(resource_dir, library)
        if os.path.isfile(absolute_library_path):
            # If we find it, don't try any other filename
            library_paths = (absolute_library_path,)
            break

    return library_paths


def _get_library_paths(os_is_nt):
    """ Override library path.
    """
    try:
        return __get_library_paths(os_is_nt)

    # Docker container (linux)
    except OSError:
        return ("libmediainfo.so.0",)


# Patch to redirect to current libraries.
from pymediainfo import MediaInfo  # pylint: disable=C0413
MediaInfo._get_library_paths = _get_library_paths  # pylint: disable=W0212

from lite_media_core._mediaInfo import _base  # pylint: disable=C0413


class MediaInfoAPI(_base.AbstractRegexIdentifier):
    """ Media Info based regex media info inspector.
    """
    _packages = ['mediainfo']

    info_video_values = {
        'width' : 'width',
        'height' : 'height',
        'pixel_aspect_ratio' : 'pixelAspectRatio',
        'duration' : 'seconds',
        'frame_rate' : 'frameRate',
        'frame_count' : 'frames',
        'commercial_name' : 'codec',
    }

    other_video_values = {
        'time_code_of_first_frame' : 'timecode',
    }

    info_audio_values = {
        'duration': 'duration_in_ms',
        'bit_rate': 'bitrate',
        'frame_rate': 'frameRate_audio',
        'sampling_rate': 'samplingRate'
    }

    info_image_values = {
        'height' : 'height',
        'pixel_aspect_ratio' : 'pixelAspectRatio',
        'width' : 'width',
    }

    @classmethod
    def getMediaInformation(cls, inputFile):
        """ Return information from provided media file.

        :param str inputFile: The media file to get information from.
        :return: The media information, metadata.
        :rtype: tuple (dict, :class:`collections.OrderedDict`)
        :raise MediaInfoException: When the provided input is not supported.
        """
        info = {}
        metadata = collections.OrderedDict()  # will store 'official' metadata upfront.
        newMedia = MediaInfo.parse(inputFile)

        for stream in newMedia.tracks:
            streamName = stream.track_type

            for key, val in stream.to_data().items():
                if val:
                    if streamName == "Video" and key in cls.info_video_values:
                        info[cls.info_video_values[key]] = val
                    elif streamName == "Image" and key in cls.info_image_values:
                        info[cls.info_image_values[key]] = val
                    elif streamName == "Other" and key in cls.other_video_values:
                        info[cls.other_video_values[key]] = val
                    elif streamName == "Audio" and key in cls.info_audio_values:
                        info[cls.info_audio_values[key]] = val
                    else:
                        if streamName not in metadata:
                            metadata[streamName] = {}
                        metadata[streamName][key] = val

        # Make sure we got some data
        try:
            assert info and metadata

        except AssertionError as error:
            raise _base.MediaInfoException("Unsupported file: %s." % inputFile) from error

        # Convert milliseconds to seconds
        if "seconds" in info:
            info["seconds"] = "%g" % (float(info["seconds"]) / 1000.0)

        return info, metadata
