import tkinter as tk
from snake_game import SnakeGame, Sign, Direction


def draw_clear(x, y):
    canvas.create_rectangle(x * snake_game.cell_size(),
                            y * snake_game.cell_size(),
                            (x + 1) * snake_game.cell_size(),
                            (y + 1) * snake_game.cell_size(),
                            fill="black")


def draw_rect_fill(x, y, color):
    draw_clear(x, y)
    canvas.create_rectangle(x * snake_game.cell_size(),
                            y * snake_game.cell_size(),
                            (x + 1) * snake_game.cell_size(),
                            (y + 1) * snake_game.cell_size(),
                            fill=color)


def draw_rect(x, y, color):
    draw_clear(x, y)
    canvas.create_rectangle(x * snake_game.cell_size() + 1,
                            y * snake_game.cell_size() + 1,
                            (x + 1) * snake_game.cell_size() - 1,
                            (y + 1) * snake_game.cell_size() - 1,
                            outline=color, width=1)


def draw_circle(x, y, color):
    draw_clear(x, y)
    canvas.create_oval(x * snake_game.cell_size(),
                       y * snake_game.cell_size(),
                       (x + 1) * snake_game.cell_size(),
                       (y + 1) * snake_game.cell_size(),
                       fill=color)


def on_update(x, y, sign):
    if (sign == Sign.WALL):
        draw_rect_fill(x, y, "gray")
    elif (sign == Sign.SNACK_BODY):
        draw_rect(x, y, "green")
    elif (sign == Sign.SNACK_HEAD):
        draw_rect_fill(x, y, "green")
    elif (sign == Sign.POINT):
        draw_circle(x, y, "brown")
    elif (sign == Sign.NONE):
        draw_clear(x, y)


def on_end():
    pass


def on_key_press(event):
    if event.keysym == "Up":
        snake_game.send_dir(Direction.UP)
    elif event.keysym == "Down":
        snake_game.send_dir(Direction.DOWN)
    elif event.keysym == "Left":
        snake_game.send_dir(Direction.LEFT)
    elif event.keysym == "Right":
        snake_game.send_dir(Direction.RIGHT)


def perform_action():
    if (snake_game.is_start()):
        snake_game.next()
        root.after(100, perform_action)


root = tk.Tk()
root.title("Snack game")
root.geometry("600x600")
root.configure(bg="black")

snake_game = SnakeGame(width=32, height=32)

canvas_width = snake_game.width() * snake_game.cell_size()
canvas_height = snake_game.height() * snake_game.cell_size()

root.geometry(f"{canvas_width}x{canvas_height}")

canvas = tk.Canvas(root, width=canvas_width,
                   height=canvas_height, highlightthickness=0, borderwidth=0, bg='black')
canvas.pack(expand=True)

snake_game.register_update(on_update)
snake_game.register_update(on_update)
snake_game.start()

root.after(2000, perform_action)

root.bind("<Up>", on_key_press)
root.bind("<Down>", on_key_press)
root.bind("<Left>", on_key_press)
root.bind("<Right>", on_key_press)

root.mainloop()
