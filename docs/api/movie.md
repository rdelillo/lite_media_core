## 📚 Movie

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

If a movie path is not a recognized video format, a `UnsupportedMimeType` exception will be raised.


```python
from lite_media_core import Movie, UnsupportedMimeType

try:
    movie = media.Movie("path/to/file.txt")

except media.UnsupportedMimeType as error:
    print(f"Not a valid video: {error}")
```

### 3. Offline `Movie`

It is possible to create a `Movie` from a path that does not exist.
The `Movie` object will be created, but video information will not be reachable.

```python
from lite_media_core import media, 

movie = media.Movie("path/to/video.mov")

try:
    print("Codec:", movie.codec)

except MediaException as error:
    if not movie.exists:
        print(f"Movie {movie.path} is offline.")
    else:
        # Something else happened.
        raise
```


## Common Use-cases


### 1. Standard vs non-standard `FrameRate`

```python
from lite_media_core import media, StandardFrameRate, FrameRate

movie = media.Movie("path/to/video.mov")

if isinstance(movie:
    print("Codec:", movie.codec)

except MediaException as error:
    if not movie.exists:
        print(f"Movie {movie.path} is offline.")
    else:
        # Something else happened.
        raise
```


### 2. Check movie embedded timecode


### 3. Check DNxHD full vs legal color range

