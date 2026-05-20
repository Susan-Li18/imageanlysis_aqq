import cv2 as cv
import numpy as np

# Help function

def to_gray(image):
    """Convert RGB image to grayscale.
    OpenCV function: 
    cv.cvtColor: color space conversion
    parameter: conversion method
    cv.COLOR_RGB2GRAY:
    - color convert
    - RGB three channel to one channel
    """
    if len(image.shape) == 3:
        return cv.cvtColor(image,cv.COLOR_RGB2GRAY) 
    return image

def apply_gaussian_blur(image,ksize=5,sigma=1.0):
    """Apply Gaussian smoothing
    parameter:
    - ksize: kernel size(must be odd)
    - sigma: sd of Gaussian distribution(control the blur)
    OpenCV function:
    cv.GaussianBlur
    - use Gaussian kernel to do convolution
    - denoisy
    """
    ksize = int(ksize)
    if ksize % 2 == 0:
        ksize += 1
        print(f"Warning: kernel size adjusted to {ksize}")
    return cv.GaussianBlur(image,(ksize,ksize),sigma)

# Sobel kernel

def sobel_edge(image,ksize=3,ksize_blur = 3,sigma =1, return_raw =False):
    """Sobel edge detection.
    
    OpenCV function: 
    cv.Sobel:
    - calculate the gradient of image in x and y direction
    
    parameter:
    - cv.CV_64F: output datatype (float 64)
    - dx = 1, dy = 0: x axis direction
    - dx = 0, dy = 1: y axis direction

    """
    if ksize not in [1,3,5,7]:
        raise ValueError(f'Sobel kernel size must be 1,3,5,7')
    gray = to_gray(image)
    blur = apply_gaussian_blur(gray,ksize_blur,sigma)
    blur_x = cv.Sobel(blur,cv.CV_64F,dx=1,dy=0,ksize=ksize)
    blur_y = cv.Sobel(blur,cv.CV_64F,dx=0,dy=1,ksize=ksize)
    
    # calculate magnitude
    magnitude = np.sqrt(blur_x**2 + blur_y**2)

    if return_raw:
        return magnitude

    # do normalization in case the magnitude is over float 64; convert to uint8 due to OpenCV require 0~255
    # it aim to show the calculate result by an image
    # in case divide with 0
    mag_norm = cv.normalize(magnitude,None,0,255,cv.NORM_MINMAX).astype(np.uint8)
    return mag_norm


# Laplacian kernel

def laplacian_edge(image,ksize = 3,ksize_blur = 3, sigma = 1, return_raw=False):
    """
    Laplacian edge detection

    OpenCV function:
    cv.Laplacian:
    - second gradient
    
    parameter:
    - cv.CV_64F: prevent data overflow
    
    """
    gray = to_gray(image)
    blur = apply_gaussian_blur(gray,ksize_blur,sigma)
    lap = cv.Laplacian(blur,cv.CV_64F,ksize=ksize)

    # absolute
    lap = np.abs(lap)

    if return_raw:
        return lap
    
    # normalization
    lap_norm = cv.normalize(lap,None,0,255,cv.NORM_MINMAX).astype(np.uint8)
    return lap_norm

def laplacian_zero_crossing(image, ksize=3, ksize_blur=3, sigma=1):
    """
    Detect edges via Laplacian zero-crossings.

    A zero-crossing occurs where the Laplacian changes sign between
    horizontally or vertically adjacent pixels. Each zero-crossing is
    scored by the max absolute value of the two pixels straddling it.
    Only the top 50% of zero-crossings by score are kept, suppressing
    weak noise-induced sign changes.

    With stronger Gaussian blur, noise zero-crossings become weak and
    fall below the median score threshold, so edge density decreases.
    Returns a binary uint8 image (0 or 255).
    """
    gray = to_gray(image)
    blur = apply_gaussian_blur(gray, ksize_blur, sigma)
    lap = cv.Laplacian(blur, cv.CV_64F, ksize=ksize)

    abs_lap = np.abs(lap)
    sign = np.sign(lap)

    # detect sign changes and score by the stronger of the two flanking pixels
    h_cross = (sign[:, :-1] * sign[:, 1:]) < 0
    h_score = np.maximum(abs_lap[:, :-1], abs_lap[:, 1:])

    v_cross = (sign[:-1, :] * sign[1:, :]) < 0
    v_score = np.maximum(abs_lap[:-1, :], abs_lap[1:, :])

    # threshold: median score of all detected zero-crossings
    all_scores = np.concatenate([h_score[h_cross].ravel(), v_score[v_cross].ravel()])
    thresh = np.median(all_scores) if len(all_scores) > 0 else 0.0

    zc = np.zeros(lap.shape, dtype=np.uint8)
    zc[:, :-1] |= (h_cross & (h_score > thresh)).astype(np.uint8)
    zc[:-1, :] |= (v_cross & (v_score > thresh)).astype(np.uint8)

    return zc * 255


# Canny detection
def canny_edge(image, low_threshold = 50, high_threshold = 150, blur_ksize = 5, blur_sigma = 1.0):
    """
    Canny edge detection pipline

    OpenCV function:
    cv.Canny
    - use two threshold to detect edge

    """ 
    gray = to_gray(image)
    blurred = apply_gaussian_blur(gray, ksize= blur_ksize, sigma= blur_sigma)
    edges = cv.Canny(blurred, low_threshold,high_threshold)
    return edges