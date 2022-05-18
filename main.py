# import keyboard.virtual_keyboard
from keyboard import virtual_keyboard
from drawing import LiveFeedDraw
from presentation_module import presenter
from tkinter import *

BACKGROUND = "#1a1a2e"
TEXT_BOX_BG = "#0f3460"
FONT_NAME = "Calibri"

window = Tk()
# TODO: change project title
window.title("PROJECT TITLE")
window.config(padx=300, pady=300, bg=BACKGROUND)
canvas = Canvas(width=200, height=224, bg=BACKGROUND, highlightthickness=0)

# TODO: some image here maybe
# iconImage = PhotoImage(file ="FILE_PATH")
title_label = Label(text="APP_NAME", bg=BACKGROUND, fg="white", font=(FONT_NAME, 22, "bold"))
title_label.config(padx=10, pady=10)
canvas.grid(column=1, row=1)

title_label.grid(row=0, column=1)
keyboard_button = Button(text="Use Keyboard", highlightthickness=0, font=(FONT_NAME, 11, "bold"),
                         borderwidth=2, background="#d4483b", fg="white", activebackground="#d4483b",
                         activeforeground="white", width=15, command=virtual_keyboard.run_keyboard)
draw_button = Button(text="Use Drawer", highlightthickness=0, font=(FONT_NAME, 11, "bold"),
                     borderwidth=2, background="#d4483b", fg="white", activebackground="#d4483b",
                     activeforeground="white", width=15, command=LiveFeedDraw.run_drawer)
presenter_button = Button(text="Use Presenter", highlightthickness=0, font=(FONT_NAME, 11, "bold"),
                          borderwidth=2, background="#d4483b", fg="white", activebackground="#d4483b",
                          activeforeground="white", width=15, command=presenter.run_presenter)
keyboard_button.grid(row=1, column=1)
draw_button.grid(row=2, column=1)
presenter_button.grid(row=3, column=1)
window.mainloop()
