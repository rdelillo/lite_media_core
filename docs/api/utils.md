# Utils

## 📚 Movie factory using `Media`

You can use the `Media.from_path` factory to create the relevant media object.

```python
from lite_media_core import Media, Audio, Image, ImageSequence, Movie
from lite_media_core import UnsupportedMimeType


try:
    media_obj = Media.from_path("/path/to/some_media.ext")

except UnsupportedMimeType as error:
    print(f"Unrecognized media path: {error}.")

else:
    if isinstance(media_obj, Movie):
        print(f"{media_obj} is a movie.")
    elif isinstance(media_obj, ImageSequence):
        print(f"{media_obj} is an image sequence.")
    elif isinstance(media_obj, Image):
        print(f"{media_obj} is a single image.")
    elif isinstance(media_obj, Audio):
        print(f"{media_obj} is an audio.")

    print(media_obj.metadata)
```


## 📂 Discover media with `mediaos`

Quickly browse folders and automatically detect media files and sequences.

| Function | Purpose |
|:---------|:--------|
| [`listdir()`](#listdir) | List a folder (non-recursive) and detect media. |
| [`walk()`](#walk) | Recursively walk directories and detect media. |
| [`identify_from_files()`](#identify_from_files) | Identify media from a list of paths. |

---

### `listdir`

List all entries in a folder (non-recursive) and identify media objects.

```python
from lite_media_core import mediaos, Media

items = mediaos.listdir("/path/to/folder")

for item in items:
    if isinstance(item, Media):
        print(f"Found media: {item.path}")

```

!!! note
    `listdir()` only lists files in the top-level folder.  
    It does **not** search recursively.

### `walk` 

Recursively walk through a directory tree and return media objects.

```python
from lite_media_core import mediaos, Media

for root, dirs, files in mediaos.walk("/path/to/root"):
    for item in files:
        if isinstance(item, Media):
            print(f"Found media: {item.path}")

```

!!! tip
    Use `isinstance(item, media.Media)` to differentiate between media and regular files.

### `identify_from_files` 

Identify media from a given list of file paths.

```python
from lite_media_core import mediaos

files = [
    "clip.mov",
    "sequence.1001.exr",
    "sequence.1002.exr",
]

medias = mediaos.identify_from_files(files)

for m in medias:
    print(f"Identified media: {m.path} (exists={m.exists})")
```

!!! warning
    Files that are not recognized as valid media will be silently ignored.


## 📄 Represent non-media sequence

```
TODO
```
