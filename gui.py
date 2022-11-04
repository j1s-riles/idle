from math import floor
from functools import partial
import tkinter as tk
import tkinter.ttk as ttk
import game
from constants import slime_type, TICK_SCALAR


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
    lbl_power["text"] = f"{app.gel.quantity:.2f}"
    window.after(ms, run_game_loop)

def buy_button(slimetype:slime_type, amt: int, lbl:ttk.Label, btn:ttk.Button):
    app.buy_slimes(slimetype=slimetype, amt=amt)
    lbl["text"] = app.slimes[slimetype].quantity
    btn["text"] = floor(app.slimes[slimetype].price_check(1))

    

lbl_power = ttk.Label(window, text="10", width=20)
lbl_gen1 = ttk.Label(window, text="Green")
lbl_gen1_amt = ttk.Label(window, text="0")
btn_gen1_buy = ttk.Button(window, text=app.slimes[slime_type.GREEN].price_check(1))
btn_gen1_buy["command"] = partial(buy_button, slime_type.GREEN, 1, lbl_gen1_amt, btn_gen1_buy)

lbl_power.grid(row=0, column=0)
lbl_gen1.grid(row=1, column=0)
lbl_gen1_amt.grid(row=1, column=1)
btn_gen1_buy.grid(row=1, column=2)

window.after(ms, run_game_loop)
window.mainloop()
