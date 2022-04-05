from .score import score


class Evaluation():
    def __init__(self, verse_list):
        self.verse_list = verse_list
        self.score = 0
        self.accent_score = 0
        self.stress_syllables_score = 0
