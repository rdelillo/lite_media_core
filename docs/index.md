---
hide:
  - navigation
  - toc
---

<!-- Style global ultra clean -->
<style>

.card {
    background: var(--card-dark);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.23);
}

.card-small {
  font-size: 95%;
}

a {
  color: var(--accent-dark);
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>

<!-- Page container -->
<div style="max-width: 1000px; margin: auto; padding: 3rem 1rem;">

<h1>lite_media_core</h1>

<p style="font-size: 1.2em; margin-top: 1rem;">
  A streamlined Python framework for developers to validate, control, and inspect media workflows.
  Built for ingest pipelines, quality control automation, final delivery checks and image sequence validation.
</p>


<!-- Hero Feature Grid -->
<div style="
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 220px;
  gap: 1rem;
  margin-top: 3rem;
  grid-template-areas:
    'feature1 feature1 feature1'
    'feature2 feature3 feature4'
    'feature5 feature6 feature7';
">

<!-- Big Hero Feature -->
<div class="card" style="padding: 2rem; border-radius: 12px; grid-area: feature1; display: flex; flex-direction: column; justify-content: center;">
  <h2 style="margin-top: 0;">Quick Start</h2>
  <p style="font-size: 1em;">Install and start validating media instantly with no configuration overhead.</p>
  <a href="quickstart/" style="
    display: inline-block;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    color: white;
    max-width: 180px;
    font-weight: 600;
    padding: 0.8em 1.5em;
    border-radius: 8px;
    text-decoration: none;
    font-size: 1em;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: background 0.3s, transform 0.2s;
  ">
    🚀 Get Started
  </a>
</div>

<!-- Small Features -->
<div style="padding: 1.5rem; border-radius: 12px; grid-area: feature2;">
  <h3 style="margin-top: 0;">🗂️ Discover media assets</h3>
  <p>Scan folders for video, audio, or image files recursively.</p>
  <a>See example</a>
</div>

<div style="padding: 1.5rem; border-radius: 12px; grid-area: feature3;">
  <h3 style="margin-top: 0;">🎞️ Video codec and frame rate</h3>
  <p>Validate codec and frame rate against specifications.</p>
  <a>See example</a>
</div>

<div style="padding: 1.5rem; border-radius: 12px; grid-area: feature7;">
  <h3 style="margin-top: 0;">🧐 Missing or corrupted frames</h3>
  <p>Identify frame gaps or corruptions in sequences.</p>
  <a>See example</a>
</div>

<div style="padding: 1.5rem; border-radius: 12px; grid-area: feature5;">
  <h3 style="margin-top: 0;">🖼️ Detect inconsistent resolutions</h3>
  <p>Quickly spot resolution anomalies across sequences.</p>
  <a>See example</a>
</div>

<div style="padding: 1.5rem; border-radius: 12px; grid-area: feature6;">
  <h3 style="margin-top: 0;">🔎 Access detailed media metadata</h3>
  <p>Retrieve complete metadata as a Python dictionary.</p>
  <a>See example</a>
</div>

<div style="padding: 1.5rem; border-radius: 12px; grid-area: feature4;">
  <h3 style="margin-top: 0;">⏱️Embedded timecodes</h3>
  <p>Extract and verify embedded video timecodes.</p>
  <a>See example</a>
</div>

</div>

<!-- Secondary Features Grid -->
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">

<div style="padding: 1.5rem; border-radius: 12px;">
  <h3 style="margin-top: 0;">And much more...</h3>
  <ul class="card-small" style="line-height: 1.8; padding-left: 0rem;">
    <li><a>Detect anamorphic images</a></li>
    <li><a>Legal vs full color range</a></li>
    <li><a>Inspect audio sample rates</a></li>
  </ul>
</div>

<div style="padding: 1.5rem; border-radius: 12px; background-color: rgba(0, 128, 255, 0.025);">
  <h3 style="margin-top: 0;">🧪 Experimental</h3>
  <ul class="card-small" style="line-height: 1.8; padding-left: 0rem;">
    <li>Load media from URLs</li>
    <li>Download and validate videos from YouTube, Vimeo, etc.</li>
  </ul>
</div>

<div class="card" style="padding: 1.5rem; border-radius: 12px;">
  <h3 style="margin-top: 0;">Need help ?</h3>
  <p style="font-style: italic;">Contributions are always welcome!</p>
  <a href="https://github.com/rdelillo/lite_media_core/issues/new" target="_blank" style="
    display: inline-block;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    color: white;
    max-width: 220px;
    font-weight: 600;
    padding: 0.8em 1.5em;
    border-radius: 8px;
    text-decoration: none;
    font-size: 1em;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: background 0.3s, transform 0.2s;
  ">
    💬 Open an Issue
  </a>
</div>

</div>


<hr style="margin-top: 4rem;">

<h2>Credits</h2>

<p>This project builds on the shoulders of amazing open-source tools:</p>

<ul style="line-height: 1.8; padding-left: 1.5rem;">
  <li><a href="https://mediaarea.net/en/MediaInfo" target="_blank">MediaInfo</a> — Cross-platform media metadata engine</li>
  <li><a href="https://github.com/justinfx/fileseq" target="_blank">fileseq</a> — Frame-based sequence management</li>
  <li><a href="https://github.com/eoyilmaz/timecode" target="_blank">timecode</a> — Timecode parsing and manipulation</li>
</ul>

<hr style="margin-top: 4rem;">

<h2>About</h2>

<p>
  <strong>lite_media_core</strong> is built by developers, for developers.<br>
  It aims to make media validation, automation, and ingestion workflows faster, simpler, and more reliable.
</p>

</div>
