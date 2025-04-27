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
    movie = Movie("path/to/file.txt")

except UnsupportedMimeType as error:
    print(f"Not a valid video: {error}")
```

### 3. Offline `Movie`

It is possible to create a `Movie` from a path that does not exist.
The `Movie` object will be created, but video information will not be reachable.

```python
from lite_media_core import Movie 

movie = Movie("path/to/video.mov")

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
from lite_media_core import Movie, FrameRate

movie = Movie("path/to/video.mov")
print(f"value: {float(movie.frame_rate)} fps")

if movie.frame_rate.is_standard:
    print(f"Standard frame rate")
    print(f"name: {movie.frame_rate.name}")

else:
    print(f"Non standard frame rate")
    print(f"Standard rates are {FrameRate.get_industry_standards()}")
```


### 2. Check movie embedded timecode

[What is an embedded timecode ?](https://pomfort.com/article/timecode-in-digital-cinematography-an-overview/)

```python
from lite_media_core import Movie

movie = Movie("path/to/video.mov")
embedded_timecode = movie.timecode

if embedded_timecode is not None:
    print(f"Movie {movie} contains an embedded timecode.")
    print(f"Embedded TC: {embedded_timecode}")
    print(f"Embedded TC (as frames): {int(embedded_timecode)}")
```


### 3. Check DNxHR full vs legal color range

[What are full and legal color ranges ?](https://www.thepostprocess.com/2019/09/24/how-to-deal-with-levels-full-vs-video/)

```python
```