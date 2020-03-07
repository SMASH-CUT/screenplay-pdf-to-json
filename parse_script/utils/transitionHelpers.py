
transitionEnum = [
    "FADE IN",
    "FADE OUT",
    "FADE UP",
    "JUMP CUT",
    "MATCH CUT",
    "SMASH MATCH CUT",
    "MATCH DISSOLVE",
    "CUT",
    "DISSOLVE",
    "FLASH CUT",
    "FREEZE FRAME",
    "IRIS IN",
    "IRIS OUT",
    "WIPE TO"
]


def checkTransition(self, text):
    for transition in transitionEnum:
        if transition in text:
            return True
    return False
