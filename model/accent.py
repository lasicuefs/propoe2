import numpy as np


def accent_pos(t):
    if t == 'Aguda':
        return 0
    elif t == 'Grave':
        return 1
    elif t == 'Esdrúxula':
        return 2


def next_accent(previous_accents):
    ts = np.amax(previous_accents).flatten().tolist()
    n_accents = []
    for t in ts:
        if t == 0:
            n_accents.append('Aguda')
        elif t == 1:
            n_accents.append('Grave')
        elif t == 2:
            n_accents.append('Esdrúxula')
    return n_accents
