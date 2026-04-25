import numpy as np
import cv2 as cv

def edge_density(edge_img, percentile = None):
    """
    calculate the proportion of the edge density in the whole image density
    parameter:
    edge_img: binary image, if magnitude image from sobel and laplacian, need percentile as a threshold
    """
    if percentile is not None:
        thresh = np.percentile(edge_img, percentile)
        binary = (edge_img >= thresh).astype(np.uint8)
    else:
        binary = (edge_img > 0).astype(np.uint8)

    total_pixels = binary.size
    edge_pixels = int(binary.sum())
    return (edge_pixels / total_pixels) * 100
    
def edge_fragments(edge_img, percentile =None, connectivity = 8):
    """
    calculate the edge fragmentation
    
    """
    if percentile is not None:
        thresh = np.percentile(edge_img, percentile)
        binary = (edge_img >= thresh).astype(np.uint8)
    else:
        binary = (edge_img  > 0).astype(np.uint8)
    
    # connection analysis
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
        binary, connectivity, cv.CV_32S
    )
    
    # remove background（label 0）
    num_fragments = num_labels - 1
    edge_pixels = int(binary.sum())
    
    if num_fragments > 0:
        # stats[0] is background，from 1
        areas = stats[1:, cv.CC_STAT_AREA]
        avg_length = float(np.mean(areas))
        max_length = float(np.max(areas))
        fragmentation_index = num_fragments / edge_pixels if edge_pixels > 0 else 0.0
    else:
        avg_length = 0.0
        max_length = 0.0
        fragmentation_index = 0.0
    
    return {
        'num_fragments': num_fragments,
        'avg_length': avg_length,
        'max_length': max_length,
        'fragmentation_index': fragmentation_index
    }

def evaluate_edge_img(edge_img, percentile=None):
    density = edge_density(edge_img, percentile)
    frag = edge_fragments(edge_img, percentile)
    
    return {
        'edge_density_pct': density,
        **frag
    }