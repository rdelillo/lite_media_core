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

```python
# TODO improve example quick start.
from lite_media_core import Resolution, Timecode

res = Resolution(1920, 1080)
tc = Timecode("00:01:00:00", 24.0)

print("Resolution:", res)  # 1920x1080
print("TimeCode as int (frame amount):", int(tc))  # 60 seconds * 24 fps = 1440
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



