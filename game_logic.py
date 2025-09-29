moves = ["bos-g", "scorpion", "block", "poke", "shark_attack", "tsunami", "snake", "mirror", "wait"]

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