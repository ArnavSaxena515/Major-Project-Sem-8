from tkinter import *
from tkinter import filedialog


class ImagePicker:
    @staticmethod
    def browse_files():
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=[

            ('image files', '.png'),
            ('image files', '.jpg'),
        ])
        return filename
