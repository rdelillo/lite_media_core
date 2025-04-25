""" Test lite_media_core._mediaInfo._media_info_api module.
"""
# pylint: disable=too-many-lines
import os
import tempfile
from datetime import datetime
import collections
import unittest

from lite_media_core._media_info import _base
from lite_media_core._media_info import _media_info_api


_mediaPath = os.path.join(
    os.path.dirname(__file__),
    "..",
    "resources",
    "media",
)
_rawPath = os.path.join(
    os.path.dirname(__file__),
    "..",
    "resources",
    "raw",
)


class Testmedia_info_api(unittest.TestCase):
    """ Test MediaInfo.
    """

    @staticmethod
    def _getModifiedTime(path, UTC=False):
        """ Helper function to retrieve the modified date of a file
            :param str path: The media file to get modified time from.
            :param bool UTC: True if we want the datetime in UTC.
            :return: Modified time of the file
            :rtype: str
        """
        if UTC:
            return datetime.utcfromtimestamp(os.path.getmtime(path)).strftime("UTC %Y-%m-%d %H:%M:%S")

        return datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")

    def test_png(self):
        """ Ensure MediaInfo can return information from a png file.
        """
        path = os.path.join(_mediaPath, "img.png")
        information = {
            "height": 64,
            "width": 64,
        }

        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )

    def test_jpg(self):
        """ Ensure MediaInfo can return information from a jpg file.
        """
        path = os.path.join(_mediaPath, "img.jpg")
        information = {
            "height": 64,
            "width": 64
        }

        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )

    def test_tiff(self):
        """ Ensure MediaInfo can return information from a tiff file.
        """
        path = os.path.join(_mediaPath, "img.tiff")
        information = {
            "height": 64,
            "width": 64
        }
      
        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )

    def test_dpx(self):
        """ Ensure MediaInfo can return information from a dpx file.
        """
        path = os.path.join(_mediaPath, "img.dpx")
        information = {
            "height": 64,
            "pixelAspectRatio": "1.000",
            "width": 64
        }
        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )

    def test_dpx_anamorphic(self):
        """ Ensure MediaInfo can return information from an anamorphic dpx file.
        """
        path = os.path.join(_mediaPath, "img-anamorphic.dpx")

        information = {
            'width': 64,
            'pixelAspectRatio': '2.000',
            'height': 64
        }
        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )

    def test_exr(self):
        """ Ensure MediaInfo can return information from an exr file.
        """
        path = os.path.join(_mediaPath, "img.exr")
        information = {
            "height": 64,
            "pixelAspectRatio": "1.000",
            "width": 64
        }
        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )

    def test_exr_anamorphic(self):
        """ Ensure MediaInfo can return information from an anamorphic exr file.
        """
        path = os.path.join(_mediaPath, "img-anamorphic.exr")
        information = {
            'width': 64,
            'pixelAspectRatio': '2.000',
            'height': 64
        }

        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0]
        )

    def test_mov(self):
        """ Ensure MediaInfo can return information from a mov file.
        """
        path = os.path.join(_mediaPath, "video.mov")
        information = {
            'width': 512,
            'codec': 'MPEG-4 Visual',
            'seconds': '0.042',
            'pixelAspectRatio': '1.000',
            'frameRate': '24.000',
            'height': 512,
            'frames': '1',
        }

        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )

    def test_psd(self):
        """ Ensure MediaInfo can return information from psd file.
        """
        path = os.path.join(_rawPath, "sample.psd")
        information = {
            'height': 1024,
            'width': 1280,
        }

        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )

    def test_unsupportedFile_fails(self):
        """ Ensure trying to get information from an unsupported file fails.
        """
        for unsupported_format in [".ari", ".r3d", ".dng", ".CR2"]:

            with tempfile.NamedTemporaryFile(delete=False, suffix=".%s" % unsupported_format) as tmpFile:
                with self.assertRaises(_base.MediaInfoException):
                    _media_info_api.MediaInfoAPI.get_media_information(
                        tmpFile.name,
                    )

    def test_mov_with_tc(self):
        """ Ensure MediaInfo can return information from a mov file.
        """
        path = os.path.join(_mediaPath, "video_with_tc.mov")
        information = {
            'width': 256,
            'codec': 'ProRes',
            'seconds': '0.083',
            'pixelAspectRatio': '1.000',
            'frameRate': '24.000',
            'height': 256,
            'frames': '2',
            'timecode' : '01:02:03:04'
        }

        self.assertEqual(
            information,
            _media_info_api.MediaInfoAPI.get_media_information(path)[0],
        )
