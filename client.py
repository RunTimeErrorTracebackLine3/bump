import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import websockets
import json
import threading

# Note: We DO NOT import game_logic here. 
# The server is the only one that needs the game logic.

class GameClient:
    def __init__(self, root):
        self.window = root
        self.window.title("Game Client")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Networking state
        self.websocket = None
        self.asyncio_loop = asyncio.new_event_loop()
        self.send_queue = asyncio.Queue()

        # --- GUI Setup ---
        self.frm = tk.Frame(master=self.window)
        self.frm.pack()

        # Status label to show game state
        self.status_label = tk.Label(self.frm, text="Connecting to server...", font=("Helvetica", 14))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        # define options and the string var (parameters for dropdown)
        self.options = ["bos-g", "scorpion", "spartan", "shark_attack", "tsunami", "snake", "mirror", "wait"]
        self.clicked_move1 = tk.StringVar()
        self.clicked_move2 = tk.StringVar()

        self.lbl_player1 = tk.Label(text="Move 1", master=self.frm)
        self.lbl_player1.grid(row=1, column=0, pady=5, padx=5)

        self.comb1 = ttk.Combobox(master=self.frm, textvariable=self.clicked_move1, values=self.options, state="readonly")
        self.comb1.grid(row=2, column=0, pady=20, padx=20)
        self.comb1.set(self.options[7])

        self.lbl_player1_move2 = tk.Label(text="Move 2", master=self.frm)
        self.lbl_player1_move2.grid(row=1, column=1)

        self.comb2 = ttk.Combobox(master=self.frm, textvariable=self.clicked_move2, values=self.options, state="readonly")
        self.comb2.grid(row=2, column=1, padx=10, pady=10)
        self.comb2.set(self.options[7])

        # Bind the functions from your original code
        self.comb1.bind("<<ComboboxSelected>>", self.on_move1_selected)
        self.comb2.bind("<<ComboboxSelected>>", self.on_move2_selected)

        # Change the submit button's command to our new network-aware function
        self.btn_submit = tk.Button(text="Submit Move", relief="groove", borderwidth=3, command=self.submit_move, master=self.frm)
        self.btn_submit.grid(row=1, column=2, padx=10, pady=5)
        self.btn_submit.config(state=tk.DISABLED) # Disable until game starts

        # Result label
        self.result_label = tk.Label(self.frm, text="", font=("Helvetica", 12), wraplength=350)
        self.result_label.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Start the networking in a separate thread
        self.network_thread = threading.Thread(target=self.start_asyncio_loop, daemon=True)
        self.network_thread.start()

    def start_asyncio_loop(self):
        """Runs the asyncio event loop in a separate thread."""
        asyncio.set_event_loop(self.asyncio_loop)
        self.asyncio_loop.run_until_complete(self.websocket_handler())

    async def websocket_handler(self):
        """Handles the websocket connection, sending, and receiving."""
        uri = "ws://localhost:8765"
        try:
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                
                # Create two tasks: one for sending, one for receiving
                receiver_task = asyncio.create_task(self.receiver_loop())
                sender_task = asyncio.create_task(self.sender_loop())
                
                await asyncio.gather(receiver_task, sender_task)
                
        except (websockets.exceptions.ConnectionClosedError, OSError) as e:
            print(f"Connection failed: {e}")
            self.schedule_gui_update(self.handle_connection_error)
        finally:
            self.websocket = None

    async def receiver_loop(self):
        """Listens for messages from the server."""
        async for message in self.websocket:
            data = json.loads(message)
            # Messages from the network thread must safely update the GUI
            # We do this by scheduling the update on the main (Tkinter) thread
            self.schedule_gui_update(self.handle_server_message, data)

    async def sender_loop(self):
        """Waits for messages to be put in the queue and sends them."""
        while True:
            message = await self.send_queue.get()
            if self.websocket:
                await self.websocket.send(json.dumps(message))
            self.send_queue.task_done()

    def submit_move(self):
        """Called by the 'Submit Move' button (Main Thread)."""
        move1 = self.clicked_move1.get()
        move2 = self.clicked_move2.get()

        # This is your logic from the original gui_logic.py
        if move1 == "spartan" or move2 == "spartan":
            move1, move2 = "block", "poke"
        elif move1 == "bos-g":
            move2 = "wait"
        elif move2 == "bos-g":
             move1 = "wait"

        message = {
            "type": "submit_move",
            "move1": move1,
            "move2": move2
        }
        
        # Add the message to the send queue
        self.send_queue.put_nowait(message)
        
        # Update GUI
        self.status_label.config(text="Move submitted! Waiting for opponent...")
        self.btn_submit.config(state=tk.DISABLED)
        self.result_label.config(text="")

    def handle_server_message(self, data):
        """This function runs in the Main (Tkinter) Thread to safely update the GUI."""
        msg_type = data.get("type")

        if msg_type == "waiting_for_opponent":
            self.status_label.config(text="Waiting for an opponent...")
        
        elif msg_type == "game_start":
            self.status_label.config(text="Game started! Make your move.")
            self.btn_submit.config(state=tk.NORMAL)
            self.result_label.config(text="")
        
        elif msg_type == "game_result":
            result_data = data.get("result_data", {})
            outcome = result_data.get("outcome", "Unknown")
            
            # Re-enable the button for the next round
            self.status_label.config(text="Round over! Make your next move.")
            self.btn_submit.config(state=tk.NORMAL)
            
            # Format a nice result string
            result_text = (
                f"--- Result: {outcome.upper()} ---\n"
                f"You ({result_data.get('player1')}, {result_data.get('player1_move2')}) "
                f"vs. "
                f"Opponent ({result_data.get('player2')}, {result_data.get('player2_move2')})"
            )
            self.result_label.config(text=result_text)
            
        elif msg_type == "opponent_disconnected":
            self.status_label.config(text="Opponent disconnected. Waiting...")
            self.btn_submit.config(state=tk.DISABLED)
            messagebox.showinfo("Opponent Left", "Your opponent has disconnected. Waiting for a new game.")
            
    def handle_connection_error(self):
        """Called if the server connection fails."""
        self.status_label.config(text="Server connection failed.")
        self.btn_submit.config(state=tk.DISABLED)
        messagebox.showerror("Connection Error", "Could not connect to the game server. Is it running?")

    def schedule_gui_update(self, func, *args):
        """Schedules a function to be run on the main Tkinter thread."""
        self.window.after(0, func, *args)

    def on_closing(self):
        """Handle window close event."""
        if self.asyncio_loop.is_running():
            self.asyncio_loop.call_soon_threadsafe(self.asyncio_loop.stop)
        self.window.destroy()

    # --- Your original GUI logic functions ---
    # These are pure GUI logic, so they work fine as-is.
    def on_move1_selected(self, event: tk.Event):
        selected_move = self.clicked_move1.get()
        new_options: list[str] = []
        if selected_move in ["spartan", "bos-g"]:
            self.comb2.config(values=[])
            self.comb2.set("")
            if selected_move == "bos-g":
                self.comb2.config(values=["wait"])
                self.comb2.set("wait")
        else:
            new_options = [move for move in self.options if selected_move != move]
            self.comb2.config(values=new_options)
            if self.clicked_move2.get() == "":
                self.comb2.set(self.options[7])

    def on_move2_selected(self, event: tk.Event):
        selected_move1 = self.clicked_move1.get()
        selected_move2 = self.clicked_move2.get()
        if selected_move2 in ["spartan"]:
            self.comb1.set("")
        elif selected_move2 == "bos-g" and selected_move1 != "wait":
            self.comb1.set("wait")

# --- Main execution ---
if __name__ == "__main__":
    window = tk.Tk()
    client_app = GameClient(window)
    window.mainloop()