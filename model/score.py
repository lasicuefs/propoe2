def jacard(a, b):
    a = set(a)
    b = set(b)
    n_intersect = len(set.intersection(a, b))
    n_union = len(set.union(a, b))
    return n_intersect/n_union


def same_stress_pos(a, b):
    return jacard(a.stress_position, b.stress_position)


def same_stress_syllable(a, b):
    return jacard(a.stress_syllables, b.stress_syllables)


def same_accent(a, accent):
    return a.accent in accent


def score(a, b, accent):
    j = same_stress_pos(a, b)
    s = same_stress_syllable(a, b)
    if accent:
        a = same_accent(a, accent)
    else:
        a = 0
    return j + s + a


if __name__ == "__main__":
    print(jacard(['1', '2', '3'], ['3', '4']))
