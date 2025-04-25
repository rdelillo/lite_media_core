""" Image module.
"""
import itertools
from typing import Union

from lite_media_core.path_utils import sequence as _sequence

from lite_media_core.media import _image_media
from lite_media_core.media import _media


class Image(_image_media.ImageMedia):
    """ Image media.
    """
    registered_mime_types = ("image",)

    def __init__(self, path: str, mime_type: str = None):
        """ Initialize a new Image object.

        :raise ValueError: When the provided path is not an image media.
        """
        super().__init__(path, mime_type=mime_type)

        if self.type not in Image.registered_mime_types:
            raise _media.UnsupportedMimeType(
                f"Cannot create an Image from {path} ({self.type}) "
                f"valid types are {self.registered_mime_types}."
            )


class ImageSequence(_image_media.ImageMedia, _sequence.Sequence):
    """ Image sequence media.
    """
    registered_mime_types = ("application", "image")

    def __init__(self, path: str, mime_type: str = None):
        """ Initialize a new ImageSequence object.

        :raise ValueError: When the provided path is not a valid image sequence.
        """
        try:
            if isinstance(path, _sequence.Sequence):
                seq_path = path
            else:
                seq_path = _sequence.Sequence.from_string(path)

        except ValueError as error:
            raise ValueError(f"Incorrect path for sequence: {path}.") from error

        # Compute internal image sequence as media object.
        self._images = []
        self._missing = []

        for seq_data, container in zip((seq_path, seq_path.missing), (self._images, self._missing)):
            for frame_path in seq_data:
                container.append(Image(frame_path))

        # Redirect internal path to first image of the sequence to compute
        # media attributes: resolution, metadata, mimetype...
        _image_media.ImageMedia.__init__(self, seq_path.start, mime_type=mime_type)

        # Keep full sequence path as internal attribute.
        _sequence.Sequence.__init__(self, seq_path._data)

    def __iter__(self):
        """ Iterate over the media path(s).
        """
        for image in self._images:
            yield image

    def __getitem__(self, key: int) -> Image:
        """ Get sequence images per index.
        """
        return self._images[key]

    def __len__(self) -> int:
        """ Get sequence length.
        """
        return len(self._images)

    @property
    def path(self) -> str:
        """ The image sequence file path (formatted).
        """
        return self.format(_sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED)

    @property
    def missing(self) -> list:
        """ The list of the missing images in the sequence.
        """
        return self._missing

    def validate(self, strict: bool = True) -> bool:
        """
        Ensure the sequence is of consistent type,
        Ensure all images have the same resolution.
        Check that it does not mix of existing and missing frames
        (either it exists or it does not).

        Note that this operation can take some time.

        :raise ValueError: When the sequence is invalid.
        """
        return _validate_sequence(self._images, strict=strict)

    def chunk(self, chunk_size: int) -> list:
        """ Chunk a provided image sequence into a list of smaller image sequence(s).

        :raise ValueError: When the provided chunk size is invalid.
        """
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ValueError(f"Invalid chunk size provided: {chunk_size}.")

        chunk_sequences = []
        chunk_images = itertools.zip_longest(*[iter(self)] * chunk_size)

        for chunk in chunk_images:
            chunk = [chunk_bit.path for chunk_bit in chunk if chunk_bit]

            if len(chunk) == 1:
                media_path, = chunk
            else:
                sequence = _sequence.Sequence.from_list(list(chunk))
                media_path = sequence.format(_sequence.PredefinedFormat.LEGACY_HASHTAG_EXTENDED)

            chunk_sequences.append(_media.Media.from_path(media_path))

        return chunk_sequences

    @classmethod
    def from_list(cls, list_data: list) -> Union[Image]:  # pylint: disable=W0221
        """ Initialize an ImageSequence or an Image object from a list.
        """
        if len(list_data) == 1:
            return Image.from_path(list_data[0])

        return cls(_sequence.Sequence.from_list(list_data))


def _validate_sequence(image_media_list: list, strict: bool = True) -> bool:
    """ Validate a list of image media.

    :raises ValueError: When the current image sequence is not valid.
    """
    try:
        # Ensure at least one image in sequence:
        if not image_media_list:
            raise ValueError("No image in sequence.")

        # Ensure all images are same mime type.
        image_types = [image.sub_type for image in image_media_list]
        if len(set(image_types)) > 1:
            raise _media.UnsupportedMimeType(f"Inconsistent file type in sequence: {set(image_types)}.")

        # Ensure either all images exist or not.
        exists = dict((image.path, image.exists) for image in image_media_list)
        if len(set(exists.values())) != 1:
            missing_frames = [path for path, exist in exists.items() if not exist]
            raise ValueError(f"Missing frames found in sequence {missing_frames}.")

        # Validate consistent resolution for existing sequence.
        if all(exists.values()):
            resolutions = [image.resolution for image in image_media_list]
            if len(set(resolutions)) > 1:
                raise ValueError(f"Inconsistent resolutions found in sequence: {set(resolutions)}.")

    except ValueError:
        if not strict:
            return False

        raise

    return True
