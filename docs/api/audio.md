## 🎧 Audio

### 1. Create an `Audio` object

```python
from lite_media_core import Audio

audio = Audio("path/to/audio.mp3")

if audio.exists:
    print("Duration (seconds):", audio.duration)
    print("Bitrate (bps):", audio.bitrate)
    print("Sampling rate (Hz):", audio.sampling_rate)
```