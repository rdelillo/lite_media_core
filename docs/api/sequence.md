## 🖼️ Image

### 1. Create an `Image` object

```python
from lite_media_core import Image

img = Image("path/to/image.png")

if img.exists:  # Check if online ?
    width, height = img.resolution
    print("Resolution:", img.resolution)
    print("Frame Range:", img.frame_range)
    print("Metadata:", img.metadata)
```

**Lazy Loading:** metadata is loaded only when accessing a property for the first time.

**Frame Extraction:** if the filename includes a frame number (e.g. `image.0125.png`), the `frame_range` is automatically set.

### 2. Check image channels

```
TODO
```

### 3. Image MIME types

Checking the media type (instead of the file extension) provides a more reliable detection — it handles casing (JPG vs jpg) and common extension variants (jpg vs jpeg).

```python
from lite_media_core import Image

jpg_img = _image_media.ImageMedia("path/to/image.JPG")
jpeg_img = _image_media.ImageMedia("path/to/image.jpeg")

assert jpg_img.type == jpeg_img.type  # "image"
assert jpg_img.sub_type == jpeg_img.sub_type  # "jpeg"
```

### 4. Anamorphic resolution

```python
from lite_media_core import Image

img = Image("path/to/anamorphic_image.exr")

if img.resolution.pixel_aspect_ratio != 1.0:
	print(f"Image {img} is anamorphic.")
```


## 🎞️ ImageSequence

`ImageSequence` groups a series of numbered images (e.g., `img.1001.exr`, `img.1002.exr`, etc.) into a single logical media object.
It supports validation, frame iteration, resolution consistency checking, and missing frame detection.

### 1. Create an `ImageSequence` object

You can create an `ImageSequence` from:

* A formatted sequence path
* A list of image paths
* [Scanning a folder with `medios`](api/utils/#discover-media-with-mediaos)

```python
from lite_media_core import ImageSequence

# From a path
seq = ImageSequence("path/to/sequence.1001-1010#.exr")

# From a list of images
seq_from_list = ImageSequence.from_list([
    "path/to/frame.0000.exr",
    "path/to/frame.0001.exr",
    "path/to/frame.0002.exr",
])
```

You can create an image sequence from path variations.
```python
from lite_media_core import ImageSequence

seq1 = ImageSequence("/path/to/sequence.1001-1010#.exr")
seq2 = ImageSequence("/path/to/a/sequence.%04d.ext [1-2, 9-10]")
seq3 = ImageSequence("/path/to/a/sequence.@@@.ext 1-5")
seq4 = ImageSequence("/path/to/a/sequence_1-5.ext")
```

### 2. Sequence properties

When accessing properties like resolution, metadata, or mime_type, ImageSequence automatically delegates the call to the first available frame.
This ensures quick access without scanning the entire sequence.

```python
from lite_media_core import ImageSequence

seq = ImageSequence("path/to/sequence.1001-1010#.exr")

# These properties are delegated to the first frame internally
print("Resolution:", seq.resolution)
print("Metadata:", seq.metadata)
print(f"MIME type: {seq.type}/{seq.sub_type}.")
```

### 3. Format sequence path

```python
# Example output: path/to/sequence.####.exr 1001-1010
print(seq.path)

print(seq.head)   # "sequence."
print(seq.tail)   # ".exr"
print(seq.padding)  # 4
```

also using some helpers:
```python
from lite_media_core import sequence
from lite_media_core import ImageSequence

seq = ImageSequence("path/to/sequence.1001-1010#.exr")
seq.format(sequence.PredefinedFormat.FFMPEG)  # path/to/sequence.%04d.exr
```

### 4. Iterate over the sequence

```python
for frame in seq:
    print(frame.path)  # frame in an Image object
```

Access a specific frame directly:
```python
from lite_media_core import ImageSequence

seq = ImageSequence("path/to/sequence.1001-1010#.exr")

print(seq.get_frame_path(1005))  # path/to/sequence.1005.exr
```

### 5. Detect missing or corrupted frames

Loop over the missing frames:
```python
from lite_media_core import ImageSequence

seq = ImageSequence("path/to/sequence.1001-1010#.exr")

for frame in seq.missing:
    print(f"Missing frame: {frame.path}")
```

Validate a sequence with the built-in validate():
```python
from lite_media_core import ImageSequence

try:
    seq = ImageSequence("path/to/inconsistent_sequence.1001-1005#.exr")
    seq.validate()

except ValueError as e:
    print(f"Inconsistent sequence detected: {e}")
```

### 6. Check inconsistent resolution

You can use the built-in `validate()` method (see above).

You can also validate frame resolutions asynchronously for **better performance on large sequences**:

```python
import asyncio
from lite_media_core import media


async def _check_resolution(frame, expected_resolution):
    """Async check for a single frame."""
    return frame.resolution == expected_resolution


async def validate_sequence_resolution(seq: media.ImageSequence):
    """Async validate that all frames match the same resolution."""

    # Use the first available frame as the reference
    expected_resolution = seq.resolution

    tasks = [
        _check_resolution(frame, expected_resolution)
        for frame in seq
    ]

    results = await asyncio.gather(*tasks)

    # Return frames that mismatch.
    return [frame for frame, is_valid in zip(seq, results) if not is_valid]


async def main():
    seq = media.ImageSequence("path/to/sequence.1001-1020#.exr")
    mismatched_frames = await validate_sequence_resolution(seq)

    if mismatched_frames:
        print(f"Frames with wrong resolution: {mismatched_frames}.")
    else:
        print("All frames have consistent resolution.")

# Run
asyncio.run(main())
```
