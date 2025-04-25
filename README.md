# lite_media_core

> A lightweight yet powerful media framework for developers.

[![Build Status](https://github.com/rdelillo/lite_media_core/actions/workflows/run_tests.yml/badge.svg)](https://github.com/rdelillo/lite_media_core/actions/workflows/run_tests.yml)
[![Lint Check](https://github.com/rdelillo/lite_media_core/actions/workflows/ruff.yml/badge.svg)](https://github.com/rdelillo/lite_media_core/actions/workflows/ruff.yml)
[![Coverage](https://codecov.io/gh/rdelillo/lite_media_core/branch/main/graph/badge.svg)](https://codecov.io/gh/rdelillo/lite_media_core)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

### ✨ What is `lite_media_core`?

`lite_media_core` is a minimalist, developer-focused Python framework for handling media operations simply and intuitively. Designed to be lightweight, easy to integrate, and powerful enough for real-world workflows.

Whether you're building media automation tools, integrating transcoding features, or extracting metadata, `lite_media_core` is here to simplify your work.

---

### 🌟 Features

- **Clean and intuitive API**: Get started in seconds
- **Developer-oriented design**: No magic, just Python
- **Plug-and-play utilities**: Covenient utils for timecode, resolution, frame rate...
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


### 🎓 For Developers

```bash
git clone https://github.com/rdelillo/lite_media_core.git
cd lite_media_core
pip install -e .[testing]
```

Run tests:
```bash
pytest
```

Run linter:
```bash
ruff check .
```

---



