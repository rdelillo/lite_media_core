""" Test lite_media_core.resolution module.
"""
import decimal
import unittest

from lite_media_core import resolution


class TestResolution(unittest.TestCase):
    """ Test basic resolution usage.
    """
    def setUp(self):
        """ Initialize testing class.
        """
        super(TestResolution, self).setUp()
        self.resObj = resolution.Resolution(1920, 1080)

    def test_basicResolution(self):
        """ Test basic resolution attributes.
        """
        width, height = self.resObj

        self.assertEqual((1920, 1080), (width, height))
        self.assertEqual((1920, 1080), (self.resObj.width, self.resObj.height))

    def test_resolution_fails(self):
        """ Ensure a resolution object cannot be initialized from wrong inputs.
        """
        self.assertRaises(
            resolution.ResolutionException,
            resolution.Resolution,
            "wrongWidth",
            "wrongHeight",
        )

    def test_pixelAspectRatio(self):
        """ Ensure a pixel aspect ratio can be set on the resolution object.
        """
        res = resolution.Resolution(1920, 1080, pixelAspectRatio=2.0)  # anamorphic
        self.assertEqual(2.0, res.pixelAspectRatio)

    def test_pixelAspectRatio_fails(self):
        """ Ensure a wrong pixel aspect ratio fails on resolution object init.
        """
        self.assertRaises(
            resolution.ResolutionException,
            resolution.Resolution,
            1920,
            1080,
            pixelAspectRatio="wrongPixelAspectRatio",
        )

    def test_aspectRatio(self):
        """ Ensure the resolution aspect ratio is correctly computed.
        """
        expected = decimal.Decimal(1920) / decimal.Decimal(1080)
        self.assertEqual(expected, self.resObj.aspectRatio)

    def test_representAsString(self):
        """ Ensure a resolution object represents correctly as string.
        """
        self.assertEqual("1920x1080", str(self.resObj))

    def test_represent(self):
        """ Ensure a resolution object represents correctly.
        """
        expected = "<Resolution 1920x1080 pixelAspectRatio=1>"
        self.assertEqual(expected, repr(self.resObj))


class TestResolutionFromString(unittest.TestCase):
    """ Test resolution creation from string.
    """
    def test_fromString(self):
        """ Ensure a resolution.Resolution object can be created from string.
        """
        expected = resolution.Resolution(1920, 1080)
        result = resolution.Resolution.fromString("1920x1080")

        self.assertEqual(expected, result)

    def test_fromString_fails(self):
        """ Ensure resolution.Resolution initialization from a wrong string fails.
        """
        self.assertRaises(
            resolution.ResolutionException,
            resolution.Resolution.fromString,
            "wrongString",
        )
