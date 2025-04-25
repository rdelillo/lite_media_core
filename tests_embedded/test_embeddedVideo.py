""" Test lite_media_core.media._embedded module.
"""
import unittest

import datetime

from lite_media_core import media


class TestEmbeddedVideo(unittest.TestCase):
    """ Test lite_media_core.media._embedded module.
    """

    @classmethod
    def setUpClass(cls):
        """ Setup url.
        """
        super().setUpClass()
        cls.url = "https://youtu.be/JWwSVOo5K_k"
        cls.embeddedVideo = media.EmbeddedVideo(cls.url)

    def test_valid_embedded(self):
        """ Ensure an embedded media can be created from a valid url.
        """
        self.assertIsInstance(self.embeddedVideo, media.EmbeddedVideo)

    def test_invalid_embedded(self):
        """ Ensure an invalid embedded url raise an error.
        """
        with self.assertRaises(media.UnsupportedUrl):
            _ = media.EmbeddedVideo("this_is_an_invalid_url")

    def test_not_media_url_embedded(self):
        """ Ensure a valid but unavailable url raise an error.
        """
        with self.assertRaises(media.UnsupportedUrl):
            _ = media.EmbeddedVideo("https://doc.qt.io/qt-6/qml-qtquick-text.html#clip-prop")       

    def test_unavailable_embedded(self):
        """ Ensure a valid but unavailable url raise an error.
        """
        with self.assertRaises(media.UnsupportedUrl):
            _ = media.EmbeddedVideo("https://www.youtube.com/watch?v=YjlDEEGRATo")

    def test_metadata(self):
        """ Ensure valid metadata can be found from the EmbeddedVideo.
        """
        self.assertIsInstance(self.embeddedVideo.metadata, dict)
        self.assertEqual(
            "https://www.youtube.com/watch?v=JWwSVOo5K_k",
            self.embeddedVideo.metadata["webpage_url"]
        )

    @unittest.skip("TODO investigate")
    def test_embedded_settings(self):
        """ Ensure the embedded video has the proper settings.
        """
        self.assertEqual(
            (
                self.url,
                "video",
                "youtube",
                "00:06:08:00",
                "vp09.00.40.08",
                "1920x1080",
                "25.0 fps",
                "1-9199"
            ),
            (
                self.embeddedVideo.path,
                self.embeddedVideo.type,
                self.embeddedVideo.subType,
                str(self.embeddedVideo.duration),
                self.embeddedVideo.codec,
                str(self.embeddedVideo.resolution),
                str(self.embeddedVideo.framerate),
                str(self.embeddedVideo.framerange),
            )
        )

    @unittest.skip("TODO investigate")
    def test_embedded_9gag(self):
        """ Ensure it works with a 9gag video.
        """
        videoUrl = "https://9gag.com/gag/a8qbZ3Z"
        video9gag = media.EmbeddedVideo(videoUrl)

        self.assertEqual(
            (
                videoUrl,
                "video",
                "9gag",
                "00:00:24:00",
                "vp9",
                "460x816",
                "24.0 fps",
                "1-575",
            ),
            (
                video9gag.path,
                video9gag.type,
                video9gag.subType,
                str(video9gag.duration),
                video9gag.codec,
                str(video9gag.resolution),
                str(video9gag.framerate),
                str(video9gag.framerange),
            )
        )

    def test_incomplete_resolve_metadata(self):
        """ Ensure an incomplete url return valid metadata.
        """
        embeddedVideo = media.EmbeddedVideo(
            "https://www.youtube.com/watch?v=tmSm-tnifVk&list=RDtmSm-tnifVk&start_radio=1",
            full_extraction=False
        )

        self.assertEqual(238.0, embeddedVideo.duration.seconds)
        self.assertTrue(isinstance(embeddedVideo.metadata["thumbnails"], list))

    def test_incomplete_resolve_performances(self):
        """ Ensure an incomplete url resolve does not take too much time.
        """
        before = datetime.datetime.now()
        _ = media.EmbeddedVideo(
            "https://www.youtube.com/watch?v=tmSm-tnifVk&list=RDtmSm-tnifVk&start_radio=1",
            full_extraction=False
        )
        now = datetime.datetime.now()
        delay = now - before

        self.assertTrue(delay.seconds < 3.0)

    def test_playlist_disable(self):
        """ Ensure the url of the playlist only returns first video.
        """
        embeddedVideo = media.EmbeddedVideo("https://www.youtube.com/watch?v=86kKFYmAMxA&list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbA&start_radio=1&rv=mm-ALweZ7tw&ab_channel=capoVEVO")
        self.assertEqual(
            "Pedro Capó, Alicia Keys, Farruko - Calma (Alicia Remix - Official Video)",
            embeddedVideo.metadata.get("title")
        )
