# lite_media_core

> A streamlined Python framework for developers to validate, control, and inspect media workflows.

[![Build Status](https://github.com/rdelillo/lite_media_core/actions/workflows/run_tests.yml/badge.svg)](https://github.com/rdelillo/lite_media_core/actions/workflows/run_tests.yml)
[![Coverage](https://codecov.io/gh/rdelillo/lite_media_core/branch/main/graph/badge.svg)](https://codecov.io/gh/rdelillo/lite_media_core)

---

**Documentation**: [https://rdelillo.github.io/lite_media_core/](https://rdelillo.github.io/lite_media_core/)

---

### ✨ What is `lite_media_core`?

`lite_media_core` is a minimalist, developer-focused Python framework for handling media operations simply and intuitively. Designed to be lightweight, easy to integrate, and powerful enough for real-world workflows.

Whether you're building media automation tools, integrating transcoding features, or scripting quick metadata checkers, `lite_media_core` helps you get there faster with less friction.

---

### 🌟 Features

- **Clean and intuitive API**: Handles [image](https://rdelillo.github.io/lite_media_core/api/sequence/#image), [image sequence](https://rdelillo.github.io/lite_media_core/api/sequence/#imagesequence), [video](https://rdelillo.github.io/lite_media_core/api/movie/#movie), [audio](https://rdelillo.github.io/lite_media_core/api/audio/#audio)... Get started in seconds
- **Powered by MediaInfo**: Delivers accurate, detailed metadata across formats
- **Plug-and-play utilities**: Built-in helpers for timecode, resolution, and frame rate settings
- **Cross-platform**: Windows, macOS, Linux
- **Tested and linted**

---

### Practical Use Cases

`lite_media_core` helps automate key media validation tasks across ingest, quality control, and delivery workflows.

- ✅ **Validate media against client specs**: Check resolution, frame rate, codec, pixel format, and embedded timecode.
- 🎞️ **Detect issues in image sequences**: Find missing frames or inconsistent resolutions before ingest or export.
- 🎬 **Inspect QuickTime files**: Verify color range settings (video vs full) or codec compatibility for web or broadcast delivery.

---

### ⚡ Quick Start

```bash
pip install lite_media_core
```

Inspect an image sequence:
```python
from lite_media_core import ImageSequence

# Load a media using lite_media_core
media = ImageSequence("/path/to/sequence.1001-1005.exr")

# Read sequence properties if it exists.
if media.exists:

    # Print basic media properties
    print(f"Loaded media: {media.path}")
    print(f"Resolution: {media.resolution}")
    print(f"Frame range: {media.frame_range}")

    # (Optional) Full metadata
    print("Full metadata:")
    print(media.metadata)
```

**More examples in the documentation:** [https://rdelillo.github.io/lite_media_core/](https://rdelillo.github.io/lite_media_core/)

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



