import tkinter as tk
from snake_game import SnakeGame, Sign

# ■□※◎

def disable_selection(event):
    return "break"


def write_text(x, y, str):
    text_box.config(state=tk.NORMAL)
    pos = f"{y + 1}.{x}"
    print(pos)
    text_box.delete(pos)
    text_box.insert(pos, str)
    text_box.config(state=tk.DISABLED)

def on_update(x, y, sign):
    if (sign == Sign.WALL):
        write_text(x, y, "※")
    elif (sign == Sign.SNACK_BODY):
        write_text(x, y, "■")
    elif (sign == Sign.SNACK_HEAD):
        write_text(x, y, "□")
    elif (sign == Sign.POINT):
        write_text(x, y, "◎")

root = tk.Tk()
root.title("Snack game")
root.geometry("600x600")

snake_game = SnakeGame()

text_box = tk.Text(root, height=snake_game.height(), width=snake_game.width(), cursor="arrow",
                   highlightthickness=0, borderwidth=0, wrap="none", bg=root.cget("bg"))
text_box.pack(fill="both", expand=True, padx=10, pady=10)

text_box.bind("<Button-1>", disable_selection)
text_box.bind("<B1-Motion>", disable_selection)
text_box.bind("<Key>", disable_selection)

for row in range(snake_game.height()):
    for column in range(snake_game.width()):
        text_box.insert(tk.END, "　")
    text_box.insert(tk.END, "\n")

text_box.config(state=tk.DISABLED)

snake_game.register_update(on_update)
snake_game.start()

root.mainloop()
