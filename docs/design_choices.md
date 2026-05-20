# Design Choices

## Topic and Learning Objective

The app covers **edge detection** — the task of locating sharp intensity transitions in an image.
The learning objective is to help users build intuition for *why* preprocessing and threshold choices matter, by observing their effects in real time on their own images.

---

## Algorithm Selection

Three classical detectors are included to highlight different mathematical approaches:

| Detector            | Core idea                                            | Key strength                                 | Key weakness                                   |
| ------------------- | ---------------------------------------------------- | -------------------------------------------- | ---------------------------------------------- |
| **Sobel**     | First-order gradient (finite differences in x and y) | Directionally interpretable, smooth response | Sensitive to noise without sufficient blur     |
| **Laplacian** | Second-order derivative (zero-crossings)             | Isotropic — no directional bias             | Very noise-sensitive; requires strong pre-blur |
| **Canny**     | Gradient + non-maximum suppression + hysteresis      | Thin, connected edges; two-threshold control | More parameters; assumes edges are thin ridges |

Placing all three in one app makes the trade-offs directly observable rather than abstract.

---

## Preprocessing: Gaussian Blur

All three detectors are preceded by a Gaussian blur step. This is a deliberate teaching choice:
derivative operators amplify high-frequency noise, so smoothing first is standard practice.
Exposing the blur kernel size and sigma as sliders lets users see the noise–detail trade-off directly.

---

## Metric Design

Three metrics are computed for each detector:

- **Edge Density (%):** fraction of pixels classified as edge.
- **Fragment Count:** number of connected components in the binary edge map. A high count relative to a simple image usually signals noise-driven over-detection.
- **Average Fragment Length (px):** mean connected-component area in pixels. Together with fragment count it reveals whether edges form long, meaningful contours or short spurious blobs.

These three numbers are enough to distinguish a clean Canny result (low count, long fragments) from a noisy Laplacian result (high count, short fragments) .

---

## Error Handling

Uploaded files are opened with `PIL.Image.open().convert("RGB")` inside a `try/except` block.
Any corrupt, truncated, or non-image file raises an exception that is caught and displayed as a Streamlit error banner, after which the app falls back to the sample image and continues running normally.

---

## Known Trade-offs and Limitations

- Metrics are parameter-free diagnostics, not ground-truth scores. They tell you *how many* edges were found and *how connected* they are, but not whether those edges are the *correct* ones.
