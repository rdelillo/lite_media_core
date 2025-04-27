## 🎬 Movie

### 1. Create a `Movie` object

```python
from lite_media_core import media

movie = media.Movie("path/to/video.mov")

print("Codec:", movie.codec)
print("Frame rate:", movie.frame_rate)
print("Duration:", movie.duration)
print("Frame range:", movie.frame_range)
print("Full metadata:", movie.metadata)
```

### 2. Handling unsupported paths

If the provided path is not a recognized video format, a UnsupportedMimeType exception is raised.

```python
from lite_media_core import Movie, UnsupportedMimeType

try:
    movie = Movie("path/to/file.txt")

except UnsupportedMimeType as error:
    print(f"Not a valid video: {error}")
```

### 3. Offline `Movie`

You can instantiate a Movie even if the file doesn't exist.
Accessing media properties will raise an exception if the file is missing.

```python
from lite_media_core import Movie, MediaException

movie = Movie("path/to/video.mov")

try:
    print("Codec:", movie.codec)
except MediaException:
    if not movie.exists:
        print(f"Movie {movie.path} is offline.")
    else:
        raise

```


## 🎯 Common Use-cases


### 1. Checking `FrameRate`

```python
from lite_media_core import Movie, FrameRate

movie = Movie("path/to/video.mov")
print(f"value: {float(movie.frame_rate)} fps")

if movie.frame_rate.is_standard:
    print(f"Standard frame rate {movie.frame_rate.name}")

else:
    print(f"Non-standard frame rate")
    print(f"Standard rates are {FrameRate.get_industry_standards()}")
```


### 2. Inspect embedded Timecode

[What is an embedded timecode ?](https://pomfort.com/article/timecode-in-digital-cinematography-an-overview/)

```python
from lite_media_core import Movie

movie = Movie("path/to/video.mov")

if movie.timecode:
    print(f"Embedded timecode: {movie.timecode}")
    print(f"As frames: {int(movie.timecode)}")

else:
    print("No embedded timecode found.")
```


### 3. Checking Color Range (Full vs Legal)

[What are full and legal color ranges ?](https://www.thepostprocess.com/2019/09/24/how-to-deal-with-levels-full-vs-video/)

```python
from lite_media_core import Movie

movie = Movie("path/to/video.mov")
colour_range = movie.metadata.get("Video", {}).get("colour_range")

if colour_range == "Limited":
    print("Movie is legal/video color range.")

elif colour_range:
    print("Movie is full color range.")

else:
    print("Undefined colour range.")

```

!!! warning
    **TODO** Metadata fields like colour_range may not always be available depending on the media file.
