import asyncio
import websockets
import json
import game_logic  # <-- Imports your game_logic.py file

# --- Server State ---
CONNECTED_CLIENTS = set()
GAME_SESSIONS = {}
WAITING_CLIENT = None

# --- Server Helper Functions ---

async def register_client(websocket):
    """
    Called when a new client connects.
    It adds them to the connected list and tries to pair them for a game.
    """
    global WAITING_CLIENT, GAME_SESSIONS, CONNECTED_CLIENTS

    CONNECTED_CLIENTS.add(websocket)
    print(f"Client connected: {websocket.remote_address}. Total clients: {len(CONNECTED_CLIENTS)}")

    if WAITING_CLIENT is None:
        # This is the first player. They have to wait.
        WAITING_CLIENT = websocket
        game_id = str(websocket.remote_address)
        websocket.game_id = game_id 
        
        GAME_SESSIONS[game_id] = {
            "player1": websocket,
            "player2": None,
            "player1_moves": None,
            "player2_moves": None
        }
        
        message = {"type": "waiting_for_opponent"}
        await websocket.send(json.dumps(message))
        
    else:
        # A player is already waiting! Start a game.
        player1 = WAITING_CLIENT
        player2 = websocket
        WAITING_CLIENT = None 
        
        game_id = player1.game_id
        websocket.game_id = game_id
        GAME_SESSIONS[game_id]["player2"] = player2
        
        # Tell both players the game is starting.
        message_p1 = {"type": "game_start", "role": "player1"}
        message_p2 = {"type": "game_start", "role": "player2"}
        
        await player1.send(json.dumps(message_p1))
        await player2.send(json.dumps(message_p2))
        print(f"Game starting between {player1.remote_address} and {player2.remote_address}")

async def unregister_client(websocket):
    """
    Called when a client disconnects. Cleans up their game.
    """
    global WAITING_CLIENT, GAME_SESSIONS, CONNECTED_CLIENTS

    if websocket in CONNECTED_CLIENTS:
        CONNECTED_CLIENTS.remove(websocket)
    print(f"Client disconnected: {websocket.remote_address}.")

    if WAITING_CLIENT == websocket:
        WAITING_CLIENT = None
        print("Waiting client disconnected.")
        return

    if hasattr(websocket, 'game_id') and websocket.game_id in GAME_SESSIONS:
        game_id = websocket.game_id
        game = GAME_SESSIONS[game_id]
        
        opponent = game["player1"] if game["player2"] == websocket else game["player2"]
            
        if opponent and opponent in CONNECTED_CLIENTS:
            message = {"type": "opponent_disconnected"}
            await opponent.send(json.dumps(message))
            
        del GAME_SESSIONS[game_id]
        print(f"Game session {game_id} closed.")

async def handle_message(websocket, message):
    """
    Processes a message from a client and updates the game state.
    """
    global GAME_SESSIONS
    
    data = json.loads(message)
    
    if not hasattr(websocket, 'game_id'):
        return # Client disconnected before game started

    game_id = websocket.game_id
    if game_id not in GAME_SESSIONS:
        return # Game session ended

    game = GAME_SESSIONS[game_id]

    if data["type"] == "submit_move":
        is_player1 = (game["player1"] == websocket)
        moves = (data["move1"], data["move2"])
        
        if is_player1:
            game["player1_moves"] = moves
            print(f"Game {game_id}: Player 1 submitted moves: {moves}")
        else:
            game["player2_moves"] = moves
            print(f"Game {game_id}: Player 2 submitted moves: {moves}")
            
        if game["player1_moves"] and game["player2_moves"]:
            print(f"Game {game_id}: Both players have moved. Calculating result...")
            
            p1_m1, p1_m2 = game["player1_moves"]
            p2_m1, p2_m2 = game["player2_moves"]
            
            #
            # --- CALLING YOUR LOGIC FILE ---
            #
            result_dict = game_logic.play_round(p1_m1, p1_m2, p2_m1, p2_m2)
            #
            # --- END ---
            #
            
            message = {
                "type": "game_result",
                "result_data": result_dict
            }
            
            await game["player1"].send(json.dumps(message))
            await game["player2"].send(json.dumps(message))
            
            # Reset moves for the next round
            game["player1_moves"] = None
            game["player2_moves"] = None

async def main_handler(websocket):
    """
    This is the main "coroutine" that runs for EVERY client.
    """
    try:
        await register_client(websocket)
        async for message in websocket:
            await handle_message(websocket, message)
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await unregister_client(websocket)

async def main():
    print("Server starting on ws://localhost:8765")
    async with websockets.serve(main_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())