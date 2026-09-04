import numpy as np

from imagedata import ImageData
from clustering import adaptive_clustering, adaptive_treshold

def filter_image(image: ImageData) -> ImageData:
    image.arr = adaptive_clustering(image.arr)
    image.arr = adaptive_treshold(image.arr, 0)
    return image

def calculate_composition(image: ImageData) -> float:
    surface = image.arr.size
    total_val = np.sum((image.arr > 0))
    quantity = 100 * total_val / surface
    return quantity

def calculate_overlap(a: ImageData, b: ImageData) -> float:
    x1, y1 = a.arr.shape
    x2, y2 = b.arr.shape

    img1 = a.arr[:min(x1, x2), :min(y1, y2)]
    img2 = b.arr[:min(x1, x2), :min(y1, y2)]

    mask1 = (img1 == 255)
    mask2 = (img2 == 255)

    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()
    quantity = float((intersection / union) * 100.0)
    return quantity
