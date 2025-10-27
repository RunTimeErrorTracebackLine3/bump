import tkinter as tk
import game_logic

window = tk.Tk()
window.title("bump")
frm = tk.Frame(master=window)
frm.grid(row=0, column=0, sticky="nsew")
def sumbit():
    player1_move1 = clicked_move1.get()
    player1_move2 = clicked_move2.get()
    game_logic.play_round(player1_move1, player1_move2)
# define options and the string var (parameters for dropdown)
options = ["bos-g", "scorpion", "spartan", "shark_attack", "tsunami", "snake", "mirror", "wait"]
clicked_move1 = tk.StringVar()
clicked_move2 = tk.StringVar()

lbl_player1 = tk.Label(text="move1") # label for move 1
lbl_player1.grid(row=0, column=0, pady=5, padx=5)

btn_player1_move1 = tk.Button(text="sumbit",relief="groove",borderwidth=3,command=sumbit) # sumbit button
btn_player1_move1.grid(row=0,column=3,padx=10,pady=5)

drop = tk.OptionMenu(window, clicked_move1, *options) # dropdown menu for move 1
drop.grid(row=1,column=0,pady=20,padx=20)

lbl_player1_move2 = tk.Label(text="move2") # label for move 2
lbl_player1_move2.grid(row=0, column=1)

drop2 = tk.OptionMenu(window, clicked_move2, *options) # dropdown menu for move 2
drop2.grid(row=1,column=1,padx=10,pady=10)

window.mainloop()