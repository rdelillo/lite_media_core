""" Test lite_media_core.mediaos module.
"""
import os
import sys
import tempfile
import unittest

from lite_media_core import media
from lite_media_core import mediaos


class TestWalk(unittest.TestCase):
    """ Test mediaos.walk feature.
    """
    def setUp(self):
        """ Initialize testing class.
            Create a temporary hierarchy of files to walk through:

            |root/
            |------ temp.mov (video)
            |------ temp.wav (audio)
            |------ temp.png (image)
            |------ temp.py
            |------ temp.csp
            |
            |-------subdir/
                    |------- seq.1001.dpx (image sequence)
                    |------- seq.1002.dpx (image sequence)
                    |------- temp.cdl
        """
        super(TestWalk, self).setUp()

        self.root = tempfile.mkdtemp()

        # Some image, video and audio files
        tempfile.NamedTemporaryFile(suffix=".mov", dir=self.root, delete=False)
        tempfile.NamedTemporaryFile(suffix=".wav", dir=self.root, delete=False)
        tempfile.NamedTemporaryFile(suffix=".png", dir=self.root, delete=False)

        # Subdir with a sequence
        imgSeqDir = tempfile.mkdtemp(dir=self.root)
        for idx in range(1001, 1003):
            open(os.path.join(imgSeqDir, "seq.%d.dpx" % idx), "a").close()  # touch file

        # And extra non-medias ones
        tempfile.NamedTemporaryFile(suffix=".py", dir=self.root, delete=False)
        tempfile.NamedTemporaryFile(suffix=".csp", dir=self.root, delete=False)
        tempfile.NamedTemporaryFile(suffix=".cdl", dir=imgSeqDir, delete=False)

    def test_walk(self):
        """ Ensure mediaos walks properly over a root directory.
        """
        walkedRoots, walkedDirs, walkedFiles = [], [], []

        # Walk through.
        for root, dirs, files in mediaos.walk(self.root):
            walkedRoots.append(root)
            walkedDirs.extend(dirs)
            walkedFiles.extend(files)

        # Filter medias and non-media files.
        medias, nonMedias = [], []
        for walkedFile in walkedFiles:
            if isinstance(walkedFile, media.Media):
                medias.append(walkedFile)
            else:
                nonMedias.append(walkedFile)

        # Should contain:
        # - 2 dirs walked (root and image sequence subdir)
        # - 1 subdir found (image sequence subdir)
        # - 4 medias (1 Movie, 1 Audio, 1 Image and 1 ImageSequence)
        # - 3 non-media files (.py, .csp and .cdl)
        self.assertEqual(
            (2, 1, 4, 3),
            (len(walkedRoots), len(walkedDirs), len(medias), len(nonMedias)),
        )


class TestIdentifyFromFiles(unittest.TestCase):
    """ Test mediaos.identify_from_files feature.
    """

    def test_idenfityFromFiles(self):
        """ Ensure medias can be identified from a provided list of file paths.
        """
        filesList = [
            "sequence_img.01.png",
            "sequence_img.02.png",
            "movie.mov",
            "file.ext",
        ]
        imgSeq, movie = mediaos.identify_from_files(filesList)  # pylint: disable=unbalanced-tuple-unpacking

        self.assertEqual(
            (True, "sequence_img.##.png 1-2"),
            (isinstance(imgSeq, media.ImageSequence), imgSeq.path),
        )
        self.assertEqual(
            (True, "movie.mov"),
            (isinstance(movie, media.Movie), movie.path),
        )
