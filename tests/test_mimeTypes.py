""" Test lite_media_core specific MIME types.
"""
import os
import unittest

from lite_media_core.path_utils.mime_types import mimetypes


_mediaPath = os.path.join(
    os.path.dirname(__file__),
    "resources",
    "media"
)


class TestRegisteredMimeTypes(unittest.TestCase):
    """ Test mime-types already registered in the system.
    """
    def test_module_inited(self):
        """ Ensure the mimetypes overrided module was inited.
        """
        self.assertTrue(mimetypes.inited)

    def test_image_png(self):
        """ Ensure a png image is correctly identified.
        """
        pngFile = os.path.join(_mediaPath, "img.png")
        mimeType, _ = mimetypes.guess_type(pngFile)

        self.assertEqual("image/png", mimeType)

    def test_image_tiff(self):
        """ Ensure a tiff image is correctly identified.
        """
        tiffFile = os.path.join(_mediaPath, "img.tiff")
        mimeType, _ = mimetypes.guess_type(tiffFile)

        self.assertEqual("image/tiff", mimeType)

    def test_video_mov(self):
        """ Ensure a video quicktime is correctly identified.
        """
        movFile = os.path.join(_mediaPath, "video.mov")
        mimeType, _ = mimetypes.guess_type(movFile)

        self.assertEqual("video/quicktime", mimeType)


class TestAdditionalMimeTypes(unittest.TestCase):
    """ Test additional mime-types defined by lite_media_core.
    """
    def test_image_dpx(self):
        """ Ensure a dpx image is correctly identified.
        """
        dpxFile = os.path.join(_mediaPath, "img.dpx")
        mimeType, _ = mimetypes.guess_type(dpxFile)

        self.assertEqual("image/x-dpx", mimeType)

    def test_image_exr(self):
        """ Ensure an exr image is correctly identified.
        """
        exrFile = os.path.join(_mediaPath, "img.exr")
        mimeType, _ = mimetypes.guess_type(exrFile)

        self.assertEqual("image/x-exr", mimeType)

    def test_image_dng(self):
        """ Ensure a dng image is correctly identified.
        """
        dngFile = os.path.join(_mediaPath, "img.dng")
        mimeType, _ = mimetypes.guess_type(dngFile)

        self.assertEqual("image/x-adobe-dng", mimeType)

    def test_image_psd(self):
        """ Ensure a psd image is correctly identified.
        """
        psdFile = os.path.join(_mediaPath, "img.psd")
        mimeType, _ = mimetypes.guess_type(psdFile)

        self.assertEqual("image/vnd.adobe.photoshop", mimeType)
