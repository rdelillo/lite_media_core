""" Abstract base media info inspector.
"""
import abc
import re
import subprocess
import shlex


class MediaInfoException(Exception):
    """ Media identification specific exception.
    """


class AbstractRegexIdentifier:
    """ Abstract regex media identifier.
        Extract media information based on third-party subprocess output.
    """
    __metaclass__ = abc.ABCMeta
    command = None

    @classmethod
    def _regex_matches(cls, regex: str, reference: str) -> dict:
        """ Helper, find regex matches in a reference string.
        """
        match = re.search(regex, reference)
        if match:
            return match.groupdict()

        return {}

    @classmethod
    @abc.abstractmethod
    def get_media_information(cls, input_path: str):
        """ Return information from provided media file.

        :raise NotImplementedError: abstract method.
        """
        raise NotImplementedError

    @classmethod
    def _run_process(cls, input_path: str) -> tuple:
        """ Run subprocess.

        :raise MediaInfoException: When subprocess fails.
        """
        command = cls.command + " " + repr(input_path)  # repr to preserve whitespaces
        arguments = shlex.split(command)

        process = subprocess.Popen(
            arguments,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        out, _ = process.communicate()
        if bool(process.returncode):
            raise MediaInfoException(f"{command} returned error code {process.returncode}.")

        return out
