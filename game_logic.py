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