""" Test lite_media_core._mediaInfo._base module.
"""
import unittest

from lite_media_core._mediaInfo import _base


class TestAbstractRegexIdentifier(unittest.TestCase):
    """ Test AbstractRegexIdentifier.
    """
    def test_regexMatch_result(self):
        """ Ensure AbstractRegexIdentifier._regexMatches can return matching regex.
        """
        regex = r"TEST   (?P<test>[\d.]+)"
        content = "TEST   123.456"

        expected = {"test": "123.456"}
        result = _base.AbstractRegexIdentifier._regexMatches(regex, content)  # pylint: disable=w0212

        self.assertEqual(expected, result)

    def test_regexMatch_None(self):
        """ Ensure AbstractRegexIdentifier._regexMatches return an empty dict when no match.
        """
        result = _base.AbstractRegexIdentifier._regexMatches(r"", "content")  # pylint: disable=w0212
        self.assertEqual({}, result)

    def test_runProcess_ok(self):
        """ Ensure AbstractRegexIdentifier can run catch process failure.
        """
        identifier = _base.AbstractRegexIdentifier
        identifier.command = "echo"
        result = identifier._runProcess("some data to out")

        self.assertTrue(result)

    def test_runProcess_fails(self):
        """ Ensure AbstractRegexIdentifier can run catch process failure.
        """
        identifier = _base.AbstractRegexIdentifier
        identifier.command = "not_a_valid_exe"

        with self.assertRaises(_base.MediaInfoException):
            identifier._runProcess("/path/to/none/existing/file")  # force fail attempting a 'ls'of a wrong file.

    def test_getMediaInformation(self):
        """ Ensure AbstractRegexIdentifier defines a getMediaInformation function.
        """
        self.assertTrue(callable(_base.AbstractRegexIdentifier.getMediaInformation))

    def test_getMediaInformation_abstract(self):
        """ Ensure AbstractRegexIdentifier.getMediaInformation needs to be implemented.
        """
        self.assertRaises(
            NotImplementedError,
            _base.AbstractRegexIdentifier.getMediaInformation,
            "/path/to/media/file",
        )
