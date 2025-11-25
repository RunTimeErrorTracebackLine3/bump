import random as r

moves = ["bos-g", "scorpion", "block", "poke", "shark_attack", "tsunami", "snake", "mirror", "wait"]

# whatevers in the right list is what the left thing beats
win_moves = {
    "bos-g": ["scorpion", "spartan", "shark_attack", "tsunami", "wait", "mirror"],
    "scorpion": ["block", "wait", "tsunami"],
    "block": ["shark_attack", "tsunami"],
    "poke": ["mirror", "wait", "shark_attack", "scorpion"],
    "shark_attack": ["tsunami", "wait", "scorpion"],
    "tsunami": ["poke", "snake", "wait"],
    "snake": ["bos-g", "scorpion", "shark_attack", "poke"],
    "mirror": ["scorpion", "shark_attack", "tsunami"],
    "wait": [""]
}

def beats(m1: str, m2: str):
    # 1 = m1 wins, 0 = draw, -1, = m2 wins
    if m1 == m2:
        return 0
    elif m2 in win_moves.get(m1, []):
        return 1
    elif m1 in win_moves.get(m2, []):
        return -1
    else:
        return 0
def beats2(p1_m2: str, p2_m2:str):
      if p1_m2 == p2_m2:
            return 0
      elif p2_m2 in win_moves.get(p1_m2, []):
            return 1
      elif p1_m2 in win_moves.get(p2_m2, []):
            return -1
      else:
            return 0
    
# TODO make it so if any players move is none make it random also make it if on the first beat there is no winner call beats2 and only call draw if beats2 is a draw.
def play_round(player1: str, player1_move2: str, player2: str = None, player2_move2: str = None, outcome: str = None, round_1_was_draw: bool = False):
    if player2 is None: # if the first player 2's move is nothing make it a random move
        player2 = r.choice(moves)
    if player2_move2 is None: # if the first player 2's move is nothing make it a random move
        player2_move2 = r.choice(moves)
    
    if player1 == "spartan":
        player1 = "block"
        player1_move2 = "poke"
        
    # BUG FIX 1: Removed colon from "spartan:"
    if player2 == "spartan": 
        player2 = "block"
        player2_move2 = "poke"  
        
    round1 = beats(player1, player2) # take in player1's first move and player2's first move and if player 1 wins reutrn 1, if player 2 moves win reutrn -1, and if it's a draw return 0.
    if round1 == 1:
        outcome = "player1 wins"
    elif round1 == -1:
         outcome = "player2 wins"
    else:
        round_1_was_draw = True
        round2 = beats2(player1_move2, player2_move2) # if round 1 is a draw start round 2 (same logic as same round 1)
        if round2 == 1:
         outcome = "player1 wins"
        
        # BUG FIX 2: Changed 'round1' to 'round2'
        elif round2 == -1: 
         outcome = "player2 wins"
        else:
            outcome = "draw"
            
    if round_1_was_draw == False: #if round1 wasnt a draw only return out the first round
        return {
          "outcome": outcome,
          "player1": player1,
          "player1_move2": player1_move2,
          "player2": player2,
          "player2_move2": player2_move2
        }
    elif round_1_was_draw == True: #if round one was a draw return the first adn second round
        return {
          "outcome": outcome,
          "result": round2, # Note: server doesn't use this, but that's ok
          "player1": player1,
          "player1_move2": player1_move2,
          "player2": player2,
          "player2_move2": player2_move2
    }

if __name__ == "__main__":
     import json
     round_result = play_round("wait", "bos-g")
     print(json.dumps(round_result, indent=1))