import cv2 as cv
import matplotlib.pyplot as plt
import processing as proc
import numpy as np


    
# overlay
def overlay(image, edges, color=(0,0,255),alpha=0.5,thickness=2):
    """
    gary background, color edge
    
    """
    gray = proc.to_gray(image)
    bg = cv.cvtColor(gray,cv.COLOR_GRAY2BGR)

    # prepare the mask
    mask = (edges >= 255) if edges.max() > 1 else (edges == 1)
    # if line width is over 1, using cv.dilate to make the edge wider
    # eg. if thickness = 2, use 2*2 kernel which value is 1 to make the edge wider
    if thickness > 1:
        kernel = np.ones((thickness, thickness),np.uint8)
        mask = cv.dilate(mask.astype(np.uint8),kernel).astype(bool)
    
    # create color edge
    overlay = np.zeros_like(bg)
    overlay[mask] = color

    # Alpha blend
    return cv.addWeighted(bg,1-alpha,overlay,alpha,0)

def overlay_magnitude(image, mag, color=(0,0,255),alpha=0.5,thickness =2, percentile = 90):
    """ 
    mag: sobel and laplacian magnitude image
    """
    # threshold the magnitude image using percentile
    thresh = np.percentile(mag,percentile)
    binary_edge = (mag >= thresh).astype(np.uint8) * 255

    # use overlay function
    return overlay(image,binary_edge,color,alpha,thickness)