import tkinter as tk
from tkinter import ttk
import game_logic

window = tk.Tk()
window.title("bump")

frm = tk.Frame(master=window)
frm.pack()

result_frm = tk.Frame(master=window)
def sumbit():
    player1_move1 = clicked_move1.get()
    player1_move2 = clicked_move2.get()
    if player1_move1 or player1_move2 == "spartan":
        game_logic.play_round("block", "poke")
    elif clicked_move1.get() == "bos-g":
        game_logic.play_round("bos-g", "wait")
    else:
        game_logic.play_round(player1_move1, player1_move2)

def on_move1_selected(event: tk.Event):
    selected_move = clicked_move1.get()
    new_options: list[str] = []
    if selected_move in ["spartan", "bos-g"]:
        comb2.config(values=[])
        comb2.set("")
    else:
        for move in options:
            if selected_move != move:
                new_options.append(move)
                comb2.set(options[7])
            else:
                continue
    comb2.config(values=new_options)

def on_move2_selected(event: tk.Event):
    selected_move1 = clicked_move1.get()
    selected_move2 = clicked_move2.get()
    if selected_move2 in ["spartan"]:
        comb1.set("")
    elif selected_move2 == "bos-g" and selected_move1 != "wait":
        comb1.set("wait")


# define options and the string var (parameters for dropdown)
options = ["bos-g", "scorpion", "spartan", "shark_attack", "tsunami", "snake", "mirror", "wait"]
clicked_move1 = tk.StringVar()
clicked_move2 = tk.StringVar()

lbl_player1 = tk.Label(text="move1",master=frm) # label for move 1
lbl_player1.grid(row=0, column=0, pady=5, padx=5)

btn_player1_move1 = tk.Button(text="sumbit",relief="groove",borderwidth=3,command=sumbit,master=frm) # sumbit button
btn_player1_move1.grid(row=0,column=3,padx=10,pady=5)

comb1 = ttk.Combobox(master=frm,textvariable=clicked_move1,values=options,state="readonly") # dropdown for move 1
comb1.grid(row=1,column=0,pady=20,padx=20)
comb1.set(options[7])

lbl_player1_move2 = tk.Label(text="move2",master=frm) # label for move 2
lbl_player1_move2.grid(row=0, column=1)

comb2 = ttk.Combobox(master=frm,textvariable=clicked_move2,values=options,state="readonly") # dropdown for move 2
comb2.grid(row=1,column=1,padx=10,pady=10)
comb2.set(options[7])

comb1.bind("<<ComboboxSelected>>", on_move1_selected)
comb2.bind("<<ComboboxSelected>>", on_move2_selected)

window.mainloop()