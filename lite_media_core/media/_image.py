""" Image module.
"""
from lite_media_core.path_utils import sequence

from lite_media_core.media import _imageMedia
from lite_media_core.media import _media


class Image(_imageMedia.ImageMedia):
    """ Image media.
    """
    registeredMimeTypes = ("image",)

    def __init__(self, path, mimeType=None):
        """ Initialize a new Image object.

        :param str path: The media file path.
        :param str mimeType: An optional media mime-type.
        :raise ValueError: When the provided path is not an image media.
        """
        super().__init__(path, mimeType=mimeType)

        if self.type not in Image.registeredMimeTypes:
            raise _media.UnsupportedMimeType("Cannot create an Image media from %s (%s) "
                "valid types are %s." % (path, self.type, Image.registeredMimeTypes))


class ImageSequence(_imageMedia.ImageMedia, sequence.Sequence):
    """ Image sequence media.
    """
    registeredMimeTypes = ("application", "image")

    def __init__(self, path, mimeType=None):
        """ Initialize a new ImageSequence object.

        :param path: The media file path or sequence.
        :type path: str or :class:`Sequence`
        :param str mimeType: An optional media mime-type.
        :raise ValueError: When the provided path is not a valid image sequence.
        """
        # Check input path is an image sequence.
        try:
            seqPath = path if isinstance(path, sequence.Sequence) else sequence.Sequence.fromString(path)
        except ValueError as error:
            error.message = "Incorrect path for sequence: %r." % path
            raise

        # Compute internal image sequence as media object.
        self._images = []
        self._missing = []
        for seqData, container in zip((seqPath, seqPath.missing), (self._images, self._missing)):
            for framePath in seqData:
                image = Image(framePath)  # image
                container.append(image)

        # Keep full sequence path as internal attribute. But override internal path to first
        # frame in order to base usual media operations on it (resolution, metadata, mimetype).
        _imageMedia.ImageMedia.__init__(self, seqPath.start, mimeType=mimeType)
        sequence.Sequence.__init__(self, seqPath._data)

    def __iter__(self):
        """ Iterate over the media path(s).

        :return: The sequence path.
        :rtype: Generator[str]
        """
        for image in self._images:
            yield image

    def __getitem__(self, key):
        """ Get images per index.

        :param int key: The item index.
        :return: the attribute stored at the given index.
        :rtype: :class:`lite_media_core.media.Media`.
        """
        return self._images[key]

    def __len__(self):
        """ Get sequence length.

        :return: the length of the sequence.
        :rtype: int.
        """
        return len(self._images)

    @property
    def path(self):
        """
        :return: The image sequence file path.
        :rtype: str
        """
        return self.format(sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED)

    @property
    def missing(self):
        """
        :return: The list of the missing frames.
        :rtype: list of :class:`lite_media_core.media.Media`
        """
        return self._missing

    def validate(self):
        """ Validate current ImageSequence object: ensure sequence is consistent type,
        does have mix of existing/missing frames and all images have the same resolution.
        Note that this operation can take some time.

        :return: True when the sequence is valid.
        :rtype: bool
        :raise ValueError: When the sequence is invalid.
        """
        return _validateSequence(self._images)  # validate consistent sequence

    @classmethod
    def fromList(cls, listData):  # pylint: disable=W0221
        """ Initialize an ImageSequence or an Image object from a list.

        :param list listData: The data to initialize the Sequence from.
        :return: The created ImageSequence or Image object.
        :rtype: :class:`ImageSequence` or :class:`Image`
        """
        if len(listData) == 1:
            return Image.fromPath(listData[0])

        return cls(sequence.Sequence.fromList(listData))


def _validateSequence(imageMedias):
    """ Validate an image sequence.

    :param imageMedias: A list of media to validate.
    :type imageMedias: list(:class:`lite_media_core.media._imageMedia.ImageMedia`)
    :return: is the provided sequence valid ?
    :rtype: bool
    :raises ValueError: When the current image sequence is not valid.
    """
    # Ensure at least one image in sequence:
    if not imageMedias:
        raise ValueError("No image in sequence.")

    # Ensure all images are same mime type.
    imageTypes = [image.subType for image in imageMedias]
    if len(set(imageTypes)) > 1:
        raise _media.UnsupportedMimeType("Inconsistent file type in sequence: %s." % set(imageTypes))

    # Ensure either all images exist or not.
    exists = dict((image.path, image.exists) for image in imageMedias)
    if len(set(exists.values())) != 1:
        missingFrames = [path for path, exist in exists.items() if not exist]
        raise ValueError("Missing frames in sequence %s." % missingFrames)

    # Validate consistent resolution for existing sequence.
    if all(exists.values()):
        resolutions = [image.resolution for image in imageMedias]
        if len(set(resolutions)) > 1:
            raise ValueError("Inconsistent resolutions found in sequence: %s." % set(resolutions))

    return True
