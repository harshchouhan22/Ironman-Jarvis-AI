from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.font import Font
from tkinter.scrolledtext import *
from Notes import file_menu
from Notes import edit_menu
from Notes import format_menu
from Notes import help_menu
from Notes import config

root = Tk()

root.title(f"Text Editor-Untiltled Made by {config.name}")
root.geometry("300x250+300+300")
root.minsize(width=400, height=400)

text = ScrolledText(root, state='normal', height=400, width=400, wrap='word', pady=2, padx=3, undo=True)
text.pack(fill=Y, expand=1)
text.focus_set()

menubar = Menu(root)

file_menu.main(root, text, menubar)
edit_menu.main(root, text, menubar)
format_menu.main(root, text, menubar)
help_menu.main(root, text, menubar)
root.mainloop()