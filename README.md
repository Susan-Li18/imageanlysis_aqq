---
title: Edge Detection Demo
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.56.0"
app_file: app.py
pinned: false
---

# Edge Detection Demo

An interactive Streamlit app that teaches edge detection concepts through hands-on parameter exploration. Users can upload their own images (or use the built-in sample) and compare three classical algorithms — Sobel, Laplacian, and Canny — side by side with live diagnostics.

Built for Assignment 2 of the Image Analysis course.

---

## Features

- Upload any PNG/JPG image, or use the built-in sample image
- Tune Gaussian blur kernel size and sigma for each detector
- Adjust Canny hysteresis thresholds (low and high) interactively
- Side-by-side comparison: original / edge map / colour overlay
- Quantitative metrics per detector: edge density, fragment count, average fragment length
- Inline interpretation of what each metric value means

---

## Local Run Instructions

**Requirements:** Python ≥ 3.11

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd image_analysis_app

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## Hugging Face Space

> 🔗 **Live demo:** *(add your HF Space URL here after deployment)*

Deployed on Hugging Face Spaces using the Streamlit SDK.

---

## Screenshots

*(Add screenshots or a short GIF here after deployment)*

---

## Known Limitations

- **Sobel / Laplacian metrics use a fixed 90th-percentile threshold** to binarise the magnitude map. This makes density values comparable across images but may not match a visually chosen threshold.
- **Large images (> ~4 MP)** may cause slow recomputation on every slider interaction; consider downscaling before uploading.
- **Transparency / RGBA images** are automatically converted to RGB on upload; the alpha channel is discarded.
- **Canny is not suited for colour images** — the app converts to greyscale before detection, so colour-specific edge information is lost.
- All three detectors work in greyscale; colour-aware edge detection (e.g. Di Zenzo gradient) is out of scope.

---

## Design Notes

See [docs/design_choices.md](docs/design_choices.md) for a short discussion of algorithm choices, metric design, and UI decisions.
