class Evaluation():

    def __init__(self):
        self.consonant_rhyme_score = 0
        self.accent_score = 0
        self.stress_score = 0
        self.rhyme_structure_score = 0
        self.score_result = 0
        self.count = 0
        self.count_rhyme = 0
        self.intern_rhyme_score = 0

    def add(self, score):
        """ Sum scores of every verse.
        """
        self.accent_score += score.accent_score
        self.stress_score += score.stress_score
        self.rhyme_structure_score += score.rhyme_structure_score
        self.score_result += score.score_result
        self.count += 1
        if score.rhyme_verse:
            self.count_rhyme += 1

    def __repr__(self):

        return ("Resultado:" +
                "\n - Estrutura Ritmica: " + str(round(self.rhyme_structure_score/self.count, 3)) +
                "\n - Silabas Tônicas: " + str(round(self.stress_score/self.count, 3)) +
                "\n - Acento: " + str(round(self.accent_score/self.count_rhyme, 3)) +
                "\n Score Resultante: " + str(round(self.score_result/self.count, 3)))
