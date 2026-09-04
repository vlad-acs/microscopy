import numpy as np
import cv2
from pathlib import Path
from PIL import Image
from customtkinter import CTkImage
from collections.abc import Callable

type PixelArray = np.typing.NDArray[np.uint8]

class ImageData(object):
    arr: PixelArray
    filepath: Path

    def __init__(self, path: Path, remove_legend = False):
        self.filepath = path

        img = Image.open(path)

        whiteband = 0
        if remove_legend:
            arr = np.asarray(img)
            height = arr.shape[0]
            for i in range(height):
                if np.all(arr[i, :, :] == 255):
                    whiteband = height - i
                    break
        
        self.arr = np.asarray(img.convert('HSV'), np.uint8)[:-whiteband, :, 2]

    def get_element(self) -> str:
        return self.filepath.stem.split(' ')[0]

    def to_pil_image(self) -> Image.Image:
        arr_3d = np.stack([np.zeros_like(self.arr), np.zeros_like(self.arr), self.arr], -1)
        rgb_arr = cv2.cvtColor(arr_3d, cv2.COLOR_HSV2RGB)
        return Image.fromarray(rgb_arr)

    def to_ctk_image(self) -> CTkImage:
        return CTkImage(light_image=self.to_pil_image(), size=(270, 200))

    def apply(self, func: Callable[[PixelArray], PixelArray]) -> ImageData:
        self.arr = func(self.arr)
        return self
