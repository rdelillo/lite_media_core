""" Test lite_media_core._mediaInfo._base module.
"""
import unittest

from lite_media_core._media_info import _base


class TestAbstractRegexIdentifier(unittest.TestCase):
    """ Test AbstractRegexIdentifier.
    """
    def test_regexMatch_result(self):
        """ Ensure AbstractRegexIdentifier._regex_matches can return matching regex.
        """
        regex = r"TEST   (?P<test>[\d.]+)"
        content = "TEST   123.456"

        expected = {"test": "123.456"}
        result = _base.AbstractRegexIdentifier._regex_matches(regex, content)  # pylint: disable=w0212

        self.assertEqual(expected, result)

    def test_regexMatch_None(self):
        """ Ensure AbstractRegexIdentifier._regex_matches return an empty dict when no match.
        """
        result = _base.AbstractRegexIdentifier._regex_matches(r"", "content")  # pylint: disable=w0212
        self.assertEqual({}, result)

    def test_run_process_ok(self):
        """ Ensure AbstractRegexIdentifier can run catch process failure.
        """
        identifier = _base.AbstractRegexIdentifier
        identifier.command = "echo"
        result = identifier._run_process("some data to out")

        self.assertTrue(result)

    def test_run_process_fails(self):
        """ Ensure AbstractRegexIdentifier can run catch process failure.
        """
        identifier = _base.AbstractRegexIdentifier
        identifier.command = "not_a_valid_exe"

        with self.assertRaises(_base.MediaInfoException):
            identifier._run_process("/path/to/none/existing/file")  # force fail attempting a 'ls'of a wrong file.

    def test_get_media_information(self):
        """ Ensure AbstractRegexIdentifier defines a get_media_information function.
        """
        self.assertTrue(callable(_base.AbstractRegexIdentifier.get_media_information))

    def test_get_media_information_abstract(self):
        """ Ensure AbstractRegexIdentifier.get_media_information needs to be implemented.
        """
        with self.assertRaises(NotImplementedError):
            _ = _base.AbstractRegexIdentifier.get_media_information(
                "/path/to/media/file",
            )
