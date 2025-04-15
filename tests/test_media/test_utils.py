import unittest

from lite_media_core import media


class TestUtils(unittest.TestCase):
    """ Test lite_media_core.media._utils module.
    """
    def test_chunkImageSequence_equalChunks(self):
        """ Ensure an image sequence can be chunked using chunkImageSequence function.
        """
        imageSequence = media.ImageSequence.fromPath('sequence.%04d.exr 1001-1010')
        expectedChunk01 = media.ImageSequence.fromPath('sequence.%04d.exr 1001-1005')
        expectedChunk02 = media.ImageSequence.fromPath('sequence.%04d.exr 1006-1010')
        chunkedSequences = media.chunkImageSequence(imageSequence, 5)

        self.assertEqual(
            [chSeq.frameRange for chSeq in chunkedSequences],
            [
                expectedChunk01.frameRange,
                expectedChunk02.frameRange,
            ]
        )

    def test_chunkImageSequence_differentChunks(self):
        """ Ensure different size chunks can be returned by chunkImageSequence
        """
        imageSequence = media.ImageSequence.fromPath('sequence.%04d.exr 1001-1010')
        expectedChunk01 = media.ImageSequence.fromPath('sequence.%04d.exr 1001-1008')
        expectedChunk02 = media.ImageSequence.fromPath('sequence.%04d.exr 1009-1010')
        chunkedSequences = media.chunkImageSequence(imageSequence, 8)

        self.assertEqual(
            [chSeq.frameRange for chSeq in chunkedSequences],
            [
                expectedChunk01.frameRange,
                expectedChunk02.frameRange,
            ]
        )

    def test_chunkImageSequence_singleChunk(self):
        """ Ensure a single chunk is returned for single frame sequences.
        """
        imageSequence = media.ImageSequence.fromPath('/path/to/sequence.1001.exr')
        chunkedSequences = media.chunkImageSequence(imageSequence, 1)

        self.assertEqual(
            chunkedSequences,
            [imageSequence]
        )
