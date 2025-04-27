# Utils

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
from lite_media_core import mediaos, media

items = mediaos.listdir("/path/to/folder")

for item in items:
    if isinstance(item, media.Media):
        print(f"Found media: {item.path}")

```

!!! note
    `listdir()` only lists files in the top-level folder.  
    It does **not** search recursively.

### `walk` 

Recursively walk through a directory tree and return media objects.

```python
from lite_media_core import mediaos, media

for root, dirs, files in mediaos.walk("/path/to/root"):
    for item in files:
        if isinstance(item, media.Media):
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