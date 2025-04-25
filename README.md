# lite_media_core

> A lightweight yet powerful media framework for developers.

[![Build Status](https://github.com/rdelillo/lite_media_core/actions/workflows/run_tests.yml/badge.svg)](https://github.com/rdelillo/lite_media_core/actions/workflows/run_tests.yml)
[![Coverage](https://codecov.io/gh/rdelillo/lite_media_core/branch/main/graph/badge.svg)](https://codecov.io/gh/rdelillo/lite_media_core)

---

### ✨ What is `lite_media_core`?

`lite_media_core` is a minimalist, developer-focused Python framework for handling media operations simply and intuitively. Designed to be lightweight, easy to integrate, and powerful enough for real-world workflows.

Whether you're building media automation tools, integrating transcoding features, or scripting quick metadata checkers, `lite_media_core` helps you get there faster with less friction.

---

### 🌟 Features

- **Clean and intuitive API**: Get started in seconds
- **Powered by MediaInfo**: Delivers accurate, detailed metadata across formats
- **Plug-and-play utilities**: Built-in helpers for timecode, resolution, and frame rate settings
- **Cross-platform**: Windows, macOS, Linux
- **Tested and linted**

---

### ⚡ Quick Start

```bash
pip install lite_media_core
```

Download sample video (optional):
<table border="0" cellspacing="0" cellpadding="0" style="border: none;">
<tr>
<td width="50%">
```bash
pip install requests
```

```python
import requests
from lite_media_core import Media, Movie

# Download a sample video from the repository
url = (
    "https://github.com/rdelillo/lite_media_core/"
    "raw/refs/heads/main/docs/quickstart.mp4"
)
output_path = "video.mp4"

response = requests.get(url, stream=True)
response.raise_for_status()

with open(output_path, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
```

</td>
<td width="75%" align="center">
    <a href="docs/quickstart.mp4"> <img src="docs/quickstart_placeholder.jpeg" alt="Example video preview" width="100%"> </a> <sub><i>Click to watch video.</i></sub>
</td>
</tr>
</table>

```python
from lite_media_core import Media, Movie

# Load the media using lite_media_core
media = Media.from_path(output_path)

# Check that the media was successfully loaded and is of type Movie
assert media.exists and isinstance(media, Movie)

# Print basic media properties
print(f"Loaded media: {media.path}")
print(f"Type: {type(media).__name__}")
print(f"Resolution: {media.resolution}")
print(f"Codec: {media.codec}")
print(f"Duration: {media.duration} ({media.duration.seconds} seconds)")

# Frame-level information
print(f"Frame rate: {media.frame_rate}")
print(f"Estimated total frames: {int(media.duration)}")

# (Optional) full metadata output
print("Full metadata:")
print(media.metadata)
```

---

### 💡 Roadmap

- [ ] Support media from URL via embedded features
- [ ] Automated batch media workflows
- [ ] Lightweight CLI or API utilities

---

### 🎁 Credits

This project builds on powerful open-source tools:

* [`MediaInfo`](https://mediaarea.net/en/MediaInfo): cross-platform media metadata engine
* [`pymediainfo`](https://github.com/sbraz/pymediainfo): python bindings to MediaInfo
* [`fileseq`](https://github.com/justinfx/fileseq): image sequence handling with frame padding
* [`timecode`](https://github.com/eoyilmaz/timecode): precise and robust timecode utilities

---

### 💻 For Developers


Clone and install in dev mode:

```bash
git clone https://github.com/rdelillo/lite_media_core.git
cd lite_media_core
pip install -e .
```

Run tests:
```bash
pip install -e .[testing]
pytest
```

Run linter:
```bash
pip install -e .[lint]
ruff check .
```

---



