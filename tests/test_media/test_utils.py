import unittest

from lite_media_core import media


class TestUtils(unittest.TestCase):
    """ Test lite_media_core.media._utils module.
    """

    def test_chunk_equals(self):
        """ Ensure an image sequence can be chunked.
        """
        image_sequence = media.ImageSequence.from_path('sequence.%04d.exr 1001-1010')
        chunk01 = media.ImageSequence.from_path('sequence.%04d.exr 1001-1005')
        chunk02 = media.ImageSequence.from_path('sequence.%04d.exr 1006-1010')
        chunks = image_sequence.chunk(5)

        self.assertEqual(
            [chSeq.frame_range for chSeq in chunks],
            [
                chunk01.frame_range,
                chunk02.frame_range,
            ]
        )

    def test_chunk_different(self):
        """ Ensure different size chunks can be returned.
        """
        image_sequence = media.ImageSequence.from_path('sequence.%04d.exr 1001-1010')
        chunk01 = media.ImageSequence.from_path('sequence.%04d.exr 1001-1008')
        chunk02 = media.ImageSequence.from_path('sequence.%04d.exr 1009-1010')
        chunks = image_sequence.chunk(8)

        self.assertEqual(
            [chSeq.frame_range for chSeq in chunks],
            [
                chunk01.frame_range,
                chunk02.frame_range,
            ]
        )

    def test_single_chunk(self):
        """ Ensure a single chunk is returned for a single frame sequence.
        """
        image_sequence = media.ImageSequence.from_path('/path/to/sequence.1001.exr')
        chunks = image_sequence.chunk(1)

        self.assertEqual(
            chunks,
            [image_sequence]
        )
