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
    def _regexMatches(cls, regex, reference):
        """ Helper, find regex matches in a reference string.

        :param str regex: The regex to run.
        :param str reference: The reference to analyze.
        :return: All regex matches as dictionary.
        :rtype: dict
        """
        match = re.search(regex, reference)
        if match:
            return match.groupdict()

        return {}

    @classmethod
    @abc.abstractmethod
    def getMediaInformation(cls, inputFile):
        """ Return information from provided media file.

        :param str inputFile: The media file to get information from.
        :raise NotImplementedError: abstract method.
        """
        raise NotImplementedError

    @classmethod
    def _runProcess(cls, inputFile):
        """ Run subprocess.

            :param str inputFile: the input media file path.
            :return:  stdout, stderr.
            :rtype: tuple: (str, str)
            :raise MediaInfoException: When subprocess fails.
        """
        command = cls.command + " " + repr(inputFile)  # repr to preserve whitespaces
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
            raise MediaInfoException("%s returned error code %d." % (command, process.returncode))

        return out
