import tkinter as tk
from tkinter import font


def resize_container(event):
    if event.widget == root:
        # window_width = event.width
        # window_height = event.height
        # side_length = min(window_width, window_height)
        # x = (window_width - side_length) // 2
        # y = (window_height - side_length) // 2
        # container.place(x=x, y=y, width=side_length, height=side_length)

        # new_font_size = max(10, event.height // 2)
        # custom_font.configure(size=new_font_size)
        pass


def on_configure(event):
    resize_container(event)


def set_text(x, y, text):
    labels[y][x].config(text=text)


root = tk.Tk()
root.title("Snake game in python with tk")
root.geometry("600x600")

rows = 32
columns = 32

container = tk.Frame(root)
container.place(x=0, y=0, width=600, height=600)

for row in range(rows):
    container.grid_rowconfigure(row, weight=1)

for column in range(columns):
    container.grid_columnconfigure(column, weight=1)


labels = []

custom_font = tk.font.Font(family="Fira code", size=24)
for row in range(rows):
    labels_column = []
    for column in range(columns):
        label = tk.Label(container, text="", font=custom_font,
                         anchor="center", justify="center")
        label.grid(row=row, column=column, sticky="nsew")
        labels_column.append(label)
    labels.append(labels_column)

# root.bind("<Configure>", on_configure)

for x in range(columns):
    set_text(x, 0, "※")

for x in range(columns):
    set_text(x, columns - 1, "※")

for y in range(1, rows - 1):
    set_text(0, y, "※")
    set_text(columns - 1, y, "※")

root.mainloop()
