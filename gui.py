from math import floor
from functools import partial
import tkinter as tk
import tkinter.ttk as ttk
import game
from constants import gen_ID, TICK_SCALAR


app = game.Game()
ms = int(TICK_SCALAR * 1000)

# Set window placement
window = tk.Tk()
w = 400
h = 200
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()

x = ws/2 - w/2
y = hs/2.5 - h/2

window.geometry('%dx%d+%d+%d' % (w, h, x, y))

def run_game_loop():
    """Runs one step of the game loop and recurses"""
    app.game_loop()
    lbl_power["text"] = f"{app.currency:.2f}"
    window.after(ms, run_game_loop)

def buy_button(g_ID: gen_ID, amt: int, lbl:ttk.Label, btn:ttk.Button):
    app.buy_generator(g_ID, amt)
    lbl["text"] = app.generators[g_ID].quantity
    btn["text"] = floor(app.generators[g_ID].cost)

    

lbl_power = ttk.Label(window, text="10", width=20)
lbl_gen1 = ttk.Label(window, text="Gen1")
lbl_gen1_amt = ttk.Label(window, text="0")
btn_gen1_buy = ttk.Button(window, text=app.generators[gen_ID.PC1].cost)
btn_gen1_buy["command"] = partial(buy_button, gen_ID.PC1, 1, lbl_gen1_amt, btn_gen1_buy)

lbl_power.grid(row=0, column=0)
lbl_gen1.grid(row=1, column=0)
lbl_gen1_amt.grid(row=1, column=1)
btn_gen1_buy.grid(row=1, column=2)

window.after(ms, run_game_loop)
window.mainloop()
