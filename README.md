Bump:
Bump is a 2-player, networked strategy game based on Rock, Paper, Scissors, but with a complex twist. Instead of one move, you and your opponent must both submit two moves at once.

This project took me 3 months to make. I hope you enjoy it!

How it Works:
Each player submits two moves.

Round 1: Your first move is played against your opponent's first move. If one player wins, the game is over.

Round 2: If Round 1 was a draw, your second moves are played against each other to decide the winner.

If Round 2 is also a draw, the entire match is a draw.

To see the full list of moves and what beats what, you can refer to the win_moves dictionary in game_logic.py.

Requirements:
Both players must have Python installed.

You will also need the websockets library. You can install it by running:

python -m pip install websockets
One player (the "Host") must also have ngrok downloaded.

How to Play (Network Setup)
This game uses a server-client model. One player must be the "Host" (Player 1), and the other is the "Client" (Player 2).

1. For the Host (Player 1)
You will need to run the server, expose it to the internet with ngrok, and then run your own client.

Start the Server: Open a terminal and run the server file:
python game_server.py

Start ngrok: Open a second terminal and run ngrok to expose your server's port (8765):
./ngrok http 8765

Get the URL: ngrok will give you a public "Forwarding" URL. It will look something like this: https://random-text.ngrok-free.dev

Send the URL: Send this URL to Player 2.

Start Your Client: Open a third terminal and run your own client:
python client.py

Your game window will open and say "Waiting for an opponent..."

2. For the Client (Player 2)
Get the URL: Get the ngrok URL from the Host (Player 1).

Edit Your Client: Open your client.py file in a text editor.

Find the URI line: Near the top, find the line that says:
uri = "ws://localhost:8765"

Update the URI: Change this line to the URL the Host sent you. You must change https:// to wss:// (for a Secure WebSocket).

For example:
uri = "wss://random-text.ngrok-free.dev"

Save and Run: Save the client.py file and run it from your terminal:
python client.py

If successful, the game will automatically start for both of you!

🚨 Troubleshooting:
If Player 2 sees a "Connection Failed" or [SSL: WRONG_VERSION_NUMBER] error, the problem is almost always on Player 2's network.

This is common on school, dorm, or office Wi-Fi, which often blocks WebSocket connections.

Solutions (for Player 2):

Antivirus/Firewall: Try temporarily disabling your local Antivirus or Firewall and see if it connects.

Change Networks: The most reliable fix is to connect your computer to a different network, like a mobile hotspot, which does not have the same firewall rules.