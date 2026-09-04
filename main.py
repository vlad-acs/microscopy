import customtkinter as ctk
from pathlib import Path
from typing import List, Tuple
from copy import deepcopy
from itertools import combinations

from interface import FilesPanel, PercentagePanel, ComparisonPanel
from imagedata import ImageData
from operations import filter_image, calculate_composition, calculate_overlap

class App(ctk.CTk):
    initial_images: List[ImageData]
    processed_images: List[ImageData]
    compositions: List[Tuple[ImageData, float]]
    overlaps: List[Tuple[ImageData, ImageData, float]]

    def __init__(self):
        super().__init__()

        self.title('Sample quantifier')
        self.geometry('1200x600')
        self.minsize(500, 500)

        self.columnconfigure(0, weight=0, minsize=300)
        self.columnconfigure(1, weight=0, minsize=500)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.files_panel = FilesPanel(self, load_callback=self.load_files, clear_callback=self.clear_files)
        self.files_panel.grid(row=0, column=0, rowspan=2, sticky='nsew')

        self.composition_panel = PercentagePanel(self)
        self.composition_panel.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        self.overlap_panel = PercentagePanel(self)
        self.overlap_panel.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        self.comparison_panel = ComparisonPanel(self)
        self.comparison_panel.grid(row=0, rowspan=2, column=2, sticky='nsew', padx=10, pady=10)

    def update(self):
        self.processed_images = [filter_image(x) for x in deepcopy(self.initial_images)]
        self.compositions = [(x, calculate_composition(x)) for x in self.processed_images]
        self.overlaps = [(x, y, calculate_overlap(x, y)) for (x, y) in combinations(self.processed_images, 2)]

        self.compositions.sort(key=lambda x : x[1], reverse=True)
        self.overlaps.sort(key=lambda x : x[2] ,reverse=True)

        self.files_panel.update_list([image.filepath.name for image in self.initial_images])
        self.composition_panel.update_list([(image.get_element(), quantity) for (image, quantity) in self.compositions])
        self.overlap_panel.update_list([(f'{img1.get_element()}-{img2.get_element()}', quantity) for (img1, img2, quantity) in self.overlaps])
        self.comparison_panel.update_list([(img1.get_element(), img1.to_ctk_image(), img2.to_ctk_image()) for (img1, img2) in zip(self.initial_images, self.processed_images)])

    def load_files(self):
        directory_path = ctk.filedialog.askdirectory()
        if not directory_path: return

        base_path = Path(directory_path)
        extensions = ['*.tif', '*.tiff']

        self.initial_images = []
        for ext in extensions:
            for file_path in base_path.glob(ext):
                try:
                    if file_path.is_file() and file_path.name.split(' ')[0] != 'Electron':
                        self.initial_images.append(ImageData(file_path, remove_legend=True))
                except Exception as e:
                    print(f"Corrupt or unreadable file {file_path.name}: {e}")

        self.update()

    def clear_files(self):
        if len(self.initial_images) == 0: return
        self.initial_images = []
        self.update()

if __name__ == '__main__':
    app = App()
    app.mainloop()
