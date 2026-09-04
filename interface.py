import customtkinter as ctk
from PIL.Image import Image
from typing import List, Tuple
from collections.abc import Callable

class FilesPanel(ctk.CTkFrame):
    def __init__(self, master, 
                 filenames: List[str] = [], 
                 clear_callback: Callable[[], None] | None = None, load_callback: Callable[[], None] | None = None, 
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.clear_btn = ctk.CTkButton(self, command=clear_callback, text='CLEAR')
        self.clear_btn.pack(side='bottom', anchor='s', fill='x', padx=10, pady=(5, 15))

        self.load_btn = ctk.CTkButton(self, command=load_callback, text='LOAD FILES')
        self.load_btn.pack(side='bottom', anchor='s', fill='x', padx=10, pady=5)

        self.names_list = ctk.CTkFrame(self)
        self.names_list.pack(expand=True, fill='both', padx=10, pady=10, ipadx=10, ipady=10)

        self.update_list(filenames)

    def update_list(self, filenames: List[str] = []):
        self.filenames = filenames
        for widget in self.names_list.winfo_children():
            widget.destroy()
        for name in filenames:
            ctk.CTkLabel(
                self.names_list, fg_color='transparent', 
                text=name
            ).pack(side='top', anchor='n')

class PercentagePanel(ctk.CTkScrollableFrame):
    def __init__(self, master, 
                 values: List[Tuple[str, float]] = [],
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.update_list(values)

    def update_list(self, values: List[Tuple[str, float]] = []):
        self.values = values
        for widget in self.winfo_children():
            widget.destroy()
        for (label, quantity) in self.values:
            ctk.CTkLabel(
                self, fg_color='transparent', 
                text=f'{label}:\t{quantity:.4f}%'
            ).pack(side='top', anchor='n')

class ComparisonPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, 
                 images: List[Tuple[str, ctk.CTkImage, ctk.CTkImage]] = [], 
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.update_list(images)

    def update_list(self, images: List[Tuple[str, ctk.CTkImage, ctk.CTkImage]] = []):
        self.images = images
        for widget in self.winfo_children():
            widget.destroy()
        for index, (label, img1, img2) in enumerate(self.images):
            ctk.CTkLabel(self, text=label).grid(row=index*2, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
            ctk.CTkLabel(self, image=img1, text='').grid(row=index*2+1, column=0, padx=5, pady=5, sticky='nsew')
            ctk.CTkLabel(self, image=img2, text='').grid(row=index*2+1, column=1, padx=5, pady=5, sticky='nsew')
