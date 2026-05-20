import streamlit as st
import cv2 as cv
from PIL import Image
import numpy as np
import processing as proc
import metrics as me


# give a title 
st.title("Edge Detection Demo")

# Sample image selector (shown only when no file is uploaded)
SAMPLE_IMAGES = {
    "🦜 Parrot": "./sample_images/parrot.jpg",
    "🦊 Fox":    "./sample_images/fox.jpg",
}

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg"])

# open the upload image, and transfer it to the np.array
if uploaded_file:
    try:
        image = Image.open(uploaded_file).convert("RGB")
    except Exception:
        st.error("⚠️ Could not open the uploaded file. Please upload a valid PNG or JPG image. Showing the sample image instead.")
        selected = st.radio("Or choose a sample image:", list(SAMPLE_IMAGES.keys()), horizontal=True)
        image = Image.open(SAMPLE_IMAGES[selected]).convert("RGB")
else:
    selected = st.radio("Or choose a sample image:", list(SAMPLE_IMAGES.keys()), horizontal=True)
    image = Image.open(SAMPLE_IMAGES[selected]).convert("RGB")

img_array = np.array(image)

# for Sobel kernel
st.markdown("### **Edge detection by Sobel kernel**")
# add the parameter control 
col1,col2 = st.columns(2)
with col1:
    ksize_blur_sob = st.slider("kernel size of Guassian", min_value=3, 
                            max_value=7, 
                            value=3,      
                            step=2, key="ksize_blur_sob")
with col2:
    sigma_sobel = st.slider("sigma",min_value=0.0, max_value=5.0,value=1.0, step=0.1, key="blur_sigma_sobel")
# image edge detection

sobel_edge_raw = proc.sobel_edge(img_array,ksize=3, ksize_blur= ksize_blur_sob,sigma = sigma_sobel, return_raw=True)
sobel_edge_norm = cv.normalize(sobel_edge_raw, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
_, sobel_edge_binary = cv.threshold(sobel_edge_norm, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
sobel_metrics = me.evaluate_edge_img(sobel_edge_binary)

# show images side by side
col1, col2 = st.columns(2)
with col1:
    st.image(img_array, caption= "Original")
with col2:
    st.image(sobel_edge_binary, caption="Edge detection by Sobel kernel (Otsu)")
m1, m2, m3 = st.columns(3)
m1.metric("Edge Density", f"{sobel_metrics['edge_density_pct']:.2f}%")
m2.metric("Fragments", f"{sobel_metrics['num_fragments']}")
m3.metric("Avg Length", f"{sobel_metrics['avg_length']:.1f}px")
st.caption(
    f"ℹ️ **Interpretation:** Edge density {sobel_metrics['edge_density_pct']:.1f}% is the fraction of edge pixels detected by Otsu auto-thresholding — "
    "increasing Gaussian blur suppresses noise and reduces edge density. "
    f"{sobel_metrics['num_fragments']} fragments with avg length {sobel_metrics['avg_length']:.0f}px: "
    "many short fragments suggest noise amplification; fewer, longer fragments indicate clean continuous contours. "
    "Increase Gaussian blur (larger kernel or sigma) to reduce noise-driven fragments."
)
# for Laplacian kernel
st.markdown("### **Edge detection by Laplacian kernel**")
# add the parameter control 
col1,col2 = st.columns(2)
with col1:
    ksize_blur_lap = st.slider("kernel size of Guassian", min_value=3, 
                            max_value=7, 
                            value=3,      
                            step=2, key="ksize_blur_lap")
with col2:
    sigma_lap = st.slider("sigma",min_value=0.0, max_value=5.0,value=1.0, step=0.1, key="blur_sigma_lap")
# image edge detection
Laplacian_edge_binary = proc.laplacian_zero_crossing(img_array,ksize=3, ksize_blur=ksize_blur_lap,sigma=sigma_lap)
lap_metrics = me.evaluate_edge_img(Laplacian_edge_binary)
# show images side by side
col1, col2 = st.columns(2)
with col1:
    st.image(img_array, caption= "Original")
with col2:
    st.image(Laplacian_edge_binary, caption="Edge detection by Laplacian (zero-crossing)")
m1, m2, m3 = st.columns(3)
m1.metric("Edge Density", f"{lap_metrics['edge_density_pct']:.2f}%")
m2.metric("Fragments", f"{lap_metrics['num_fragments']}")
m3.metric("Avg Length", f"{lap_metrics['avg_length']:.1f}px")
st.caption(
    f"ℹ️ **Interpretation:** Laplacian detects zero-crossings of the second derivative — it is highly sensitive to noise. "
    f"Edge density {lap_metrics['edge_density_pct']:.1f}% with {lap_metrics['num_fragments']} fragments: "
    "a high fragment count (especially compared with Canny) signals over-detection driven by noise. "
    "Increase the Gaussian blur sigma before applying the Laplacian to suppress spurious responses."
)
# for Canny detection
st.markdown("### **Edge detection by Canny**")
# add the parameter control 
col1,col2 = st.columns(2)
with col1:
    blur_ksize = st.slider("kernel size", min_value=3, 
                            max_value=7, 
                            value=3,      
                            step=2, key="blur_ksize")
    blur_sigma = st.slider("sigma",min_value=0.0, max_value=5.0,value=1.0, step=0.1, key="blur_sigma") # value is default value
with col2:
    low_threshold= st.slider("low threshold",0, 150,50,1,key="low_thr")
    high_threshold = st.slider("high threshold",0, 300, 150,1,key="high_thr")
# image edge detection
canny_edge = proc.canny_edge(img_array,low_threshold,high_threshold,blur_ksize,blur_sigma)
canny_metrics = me.evaluate_edge_img(canny_edge)
# show images side by side
col1, col2 = st.columns(2)
with col1:
    st.image(img_array, caption= "Original")
with col2:
    st.image(canny_edge, caption="Edge detection by Canny")
m1, m2, m3 = st.columns(3)
m1.metric("Edge Density", f"{canny_metrics['edge_density_pct']:.2f}%")
m2.metric("Fragment", f"{canny_metrics['num_fragments']}")
m3.metric("Avg Length", f"{canny_metrics['avg_length']:.1f}px")
st.caption(
    f"ℹ️ **Interpretation:** Canny uses hysteresis thresholding (low={low_threshold}, high={high_threshold}) to keep only strong, "
    "connected edge pixels. "
    f"Edge density {canny_metrics['edge_density_pct']:.1f}% with {canny_metrics['num_fragments']} fragments "
    f"(avg {canny_metrics['avg_length']:.0f}px): raising the high threshold suppresses weak edges and reduces fragment count; "
    "a high/low ratio ≥ 2 is a common starting point for natural images."
)