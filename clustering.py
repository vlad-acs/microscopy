import numpy as np
import cv2
from scipy.ndimage import gaussian_filter

from imagedata import PixelArray

def adaptive_treshold(arr: PixelArray, thresh: float = 15) -> PixelArray:
    threshold = (arr[arr > thresh]).mean() * 0.8
    mask = cv2.threshold(arr, threshold, 255, cv2.THRESH_BINARY)[1]
    mask = (mask > 0)
    
    output = np.zeros_like(arr)
    output[mask] = 255
    
    return output

def saturated_clustering(arr: PixelArray, baseline_mask: np.typing.NDArray[np.bool_]) -> np.typing.NDArray[np.bool_]:
    empty_pockets = (~baseline_mask).astype(np.uint8)
    dist_from_empty = cv2.distanceTransform(empty_pockets, cv2.DIST_L2, 5)
    max_dist = dist_from_empty.max()
    if max_dist > 0:
        cluster_mask = dist_from_empty > (max_dist * 0.12)
        cluster_mask = (~cluster_mask)
    else:
        cluster_mask = np.zeros_like(arr, dtype=bool)
    
    return cluster_mask

def sparse_clustering(arr: PixelArray, baseline_mask: np.typing.NDArray[np.bool_]) -> np.typing.NDArray[np.bool_]:
    bg_distance = cv2.distanceTransform((~baseline_mask).astype(np.uint8), cv2.DIST_L2, 5)
    max_bg_gap = np.percentile(bg_distance[bg_distance > 0], 75) if np.any(bg_distance > 0) else 10

    density_radius = max(3.0, float(max_bg_gap * 0.75))
    density_map = gaussian_filter(baseline_mask.astype(float), sigma=density_radius)
    if density_map.max() > 0:
        density_map /= density_map.max()
    
    density_map_8u = (density_map * 255).astype(np.uint8)
    density_threshold_8u, _ = cv2.threshold(density_map_8u[baseline_mask], 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
    density_threshold = (density_threshold_8u / 255.0) * 0.85
    cluster_mask = density_map >= density_threshold

    k_size = max(3, int(density_radius / 2) | 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k_size, k_size))
    cluster_mask = cv2.morphologyEx(cluster_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel).astype(bool)

    return cluster_mask

def adaptive_clustering(arr: PixelArray, thresh: float = 15) -> PixelArray:
    baseline_mask = cv2.threshold(arr, thresh, 255, cv2.THRESH_BINARY)[1] > 0
    total_pixels = arr.size
    active_pixels = np.sum(baseline_mask)
    occupancy_ratio = active_pixels / total_pixels

    if occupancy_ratio > 0.80: return arr

    cluster_mask = saturated_clustering(arr, baseline_mask) if occupancy_ratio > 0.60 else sparse_clustering(arr, baseline_mask)

    labels_count, labels_image, stats, _ = cv2.connectedComponentsWithStats(cluster_mask.astype(np.uint8))
    
    min_area = max(20, int((arr.shape[0] * arr.shape[1]) * 0.0002))
    
    output_mask = np.zeros_like(cluster_mask)
    for i in range(1, labels_count):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            output_mask[labels_image == i] = True
    
    output = np.zeros_like(arr)
    output[output_mask] = arr[output_mask]
    
    return output
