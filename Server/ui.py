from tkinter import *

class UI(Frame):
    def __init__(self, parent, **kwargs):
        kwargs['bg'] = "#222222"
        super().__init__(parent, **kwargs)

        parent.title("E-Election Management")
        parent.minsize(1280, 720)
        parent.state("zoomed")