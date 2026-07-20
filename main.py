import tkinter as tk
import random

WIDTH = 380
HEIGHT = 560

expression = ""
exploding = False

# ==========================================================
# Window
# ==========================================================
root = tk.Tk()
root.title("Calculator")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="#595959")
root.resizable(False, False)

# ==========================================================
# Calculator Body
# ==========================================================
body = tk.Frame(
    root,
    bg="#7b7b7b",
    bd=10,
    relief="raised"
)
body.pack(fill="both", expand=True, padx=10, pady=10)

# ==========================================================
# Display
# ==========================================================
display_var = tk.StringVar()

display_frame = tk.Frame(
    body,
    bg="#3f4630",
    bd=6,
    relief="sunken"
)
display_frame.pack(fill="x", padx=15, pady=(15, 10))

display = tk.Entry(
    display_frame,
    textvariable=display_var,
    font=("Courier New", 28, "bold"),
    justify="right",
    bg="#d4ddb3",
    fg="black",
    bd=0,
    insertbackground="black"
)
display.pack(fill="x", padx=8, pady=8, ipady=12)

tk.Label(
    body,
    text="ELMORE CALCULATOR-88",
    bg="#7b7b7b",
    fg="white",
    font=("Arial", 10, "bold")
).pack()

tk.Label(
    body,
    text="Professional Edition",
    bg="#7b7b7b",
    fg="#dddddd",
    font=("Arial", 8)
).pack(pady=(0, 10))

# ==========================================================
# Explosion Canvas
# ==========================================================
canvas = tk.Canvas(
    body,
    bg="#7b7b7b",
    highlightthickness=0
)

# Hidden until division by zero happens
canvas.place_forget()

# ==========================================================
# Functions
# ==========================================================
def press(value):
    global expression

    if exploding:
        return

    expression += str(value)
    display_var.set(expression)


def clear():
    global expression

    if exploding:
        return

    expression = ""
    display_var.set("")


def backspace():
    global expression

    if exploding:
        return

    expression = expression[:-1]
    display_var.set(expression)


def disable_buttons():
    for widget in button_frame.winfo_children():
        widget.config(state="disabled")


def create_fire_particles():
    canvas.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )

    canvas.delete("boom")

    for _ in range(150):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        size = random.randint(8, 30)

        color = random.choice([
            "#ff0000",
            "#ff5500",
            "#ff8800",
            "#ffaa00",
            "#ffff00",
            "#ffffff"
        ])

        canvas.create_oval(
            x,
            y,
            x + size,
            y + size,
            fill=color,
            outline="",
            tags="boom"
        )


def shake_window(count=30):
    if count <= 0:
        return

    dx = random.randint(-15, 15)
    dy = random.randint(-15, 15)

    x = root.winfo_x()
    y = root.winfo_y()

    root.geometry(
        f"{WIDTH}x{HEIGHT}+{x + dx}+{y + dy}"
    )

    root.after(
        40,
        lambda: shake_window(count - 1)
    )


def flash(count=12):
    if count <= 0:
        root.configure(bg="#595959")
        body.configure(bg="#7b7b7b")
        return

    color = "red" if count % 2 else "#7b7b7b"

    root.configure(bg=color)
    body.configure(bg=color)

    root.after(
        100,
        lambda: flash(count - 1)
    )


def explode():
    global exploding

    exploding = True

    disable_buttons()

    display_var.set("DIVIDE BY ZERO")

    create_fire_particles()

    shake_window()
    flash()

    root.after(
        1000,
        lambda: display_var.set("SYSTEM FAILURE")
    )

    root.after(
        2200,
        lambda: display_var.set("GOODBYE")
    )

    # Calculator destroyed
    root.after(
        3500,
        root.destroy
    )


def calculate():
    global expression

    if exploding:
        return

    try:
        result = eval(expression)

        expression = str(result)
        display_var.set(expression)

    except ZeroDivisionError:
        explode()

    except Exception:
        display_var.set("ERROR")
        expression = ""


# ==========================================================
# Buttons
# ==========================================================
button_frame = tk.Frame(
    body,
    bg="#7b7b7b"
)
button_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

buttons = [
    ["C", "⌫", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "="]
]

for i in range(5):
    button_frame.rowconfigure(i, weight=1)

for j in range(4):
    button_frame.columnconfigure(j, weight=1)

for r, row in enumerate(buttons):
    for c, text in enumerate(row):

        if text == "=":
            command = calculate
            color = "#c9b36b"

        elif text == "C":
            command = clear
            color = "#b87a7a"

        elif text == "⌫":
            command = backspace
            color = "#bdbdbd"

        else:
            command = lambda t=text: press(t)
            color = "#d5d5d5"

        # Large zero button
        if text == "0":
            button = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 18, "bold"),
                bg=color,
                relief="raised",
                bd=5,
                activebackground="#ffffff"
            )

            button.grid(
                row=r,
                column=0,
                columnspan=2,
                sticky="nsew",
                padx=5,
                pady=5
            )
            continue

        # Skip occupied cell from the large zero button
        if r == 4 and c == 1:
            continue

        actual_col = c
        if r == 4 and c > 1:
            actual_col += 1

        button = tk.Button(
            button_frame,
            text=text,
            command=command,
            font=("Arial", 18, "bold"),
            bg=color,
            relief="raised",
            bd=5,
            activebackground="#ffffff"
        )

        button.grid(
            row=r,
            column=actual_col,
            sticky="nsew",
            padx=5,
            pady=5
        )

# ==========================================================
# Start
# ==========================================================
root.mainloop()
