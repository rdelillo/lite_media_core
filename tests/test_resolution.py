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
        self.resolution_obj = resolution.Resolution(1920, 1080)

    def test_basicResolution(self):
        """ Test basic resolution attributes.
        """
        width, height = self.resolution_obj

        self.assertEqual((1920, 1080), (width, height))
        self.assertEqual(
            (1920, 1080),
            (self.resolution_obj.width, self.resolution_obj.height)
        )

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
        res = resolution.Resolution(1920, 1080, pixel_aspect_ratio=2.0)  # anamorphic
        self.assertEqual(2.0, res.pixel_aspect_ratio)

    def test_pixelAspectRatio_fails(self):
        """ Ensure a wrong pixel aspect ratio fails on resolution object init.
        """
        with self.assertRaises(resolution.ResolutionException):
            _ = resolution.Resolution(
                    1920,
                    1080,
                    pixel_aspect_ratio="wrong_pa",
                )

    def test_aspectRatio(self):
        """ Ensure the resolution aspect ratio is correctly computed.
        """
        expected = decimal.Decimal(1920) / decimal.Decimal(1080)
        self.assertEqual(expected, self.resolution_obj.aspect_ratio)

    def test_representAsString(self):
        """ Ensure a resolution object represents correctly as string.
        """
        self.assertEqual("1920x1080", str(self.resolution_obj))

    def test_represent(self):
        """ Ensure a resolution object represents correctly.
        """
        expected = "<Resolution 1920x1080 pixelAspectRatio=1>"
        self.assertEqual(expected, repr(self.resolution_obj))


class TestResolutionFromString(unittest.TestCase):
    """ Test resolution creation from string.
    """
    def test_from_string(self):
        """ Ensure a resolution.Resolution object can be created from string.
        """
        expected = resolution.Resolution(1920, 1080)
        result = resolution.Resolution.from_string("1920x1080")

        self.assertEqual(expected, result)

    def test_from_string_fails(self):
        """ Ensure resolution.Resolution initialization from a wrong string fails.
        """
        self.assertRaises(
            resolution.ResolutionException,
            resolution.Resolution.from_string,
            "wrongString",
        )
