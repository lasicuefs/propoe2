class Evaluation:
    # TODO: define the type of the attributes

    def __init__(self) -> None:
        self.consonant_rhyme_score = 0
        self.accent_score = 0
        self.stress_score = 0
        self.rhyme_structure_score = 0
        self.score_result = 0
        self.count = 0
        self.count_rhyme = 0
        self.intern_rhyme_score = 0

    def poem_scores(self, scores:list):
        for score in scores:
            if score:
                self.add(score)
        self.setFinalScore()


    def add(self, score) -> None:
        # TODO: define the type of score
        """Sum scores of every verse."""
        self.consonant_rhyme_score += score.consonant_rhyme_score
        self.accent_score += score.accent_score
        self.stress_score += score.stress_score
        self.rhyme_structure_score += score.rhyme_structure_score
        self.score_result += score.score_result
        self.intern_rhyme_score += score.intern_rhyme_score
        self.count += 1
        if score.rhyme_verse:
            self.count_rhyme += 1

    def __repr__(self) -> str:
        return (
            "Resultado:"
            + "\n - Estrutura Ritmica: "
            + str(self.rhyme_structure_score)
            + "\n - Silabas Tônicas: "
            + str(self.stress_score)
            + "\n - Acento: "
            + str(self.accent_score)
            + "\n - Rima Interna: "
            + str(self.intern_rhyme_score)
            + "\n - Rima Toante & Consoante: "
            + str(self.consonant_rhyme_score)
            + "\n Score Resultante: "
            + str(self.score_result)
        )

    def setFinalScore(self):
        if self.rhyme_structure_score != 0:
            self.rhyme_structure_score = round(self.rhyme_structure_score / self.count, 3)
        if self.stress_score != 0:
            self.stress_score = round(self.stress_score / self.count, 3)
        if self.accent_score != 0:
            self.accent_score = round(self.accent_score / self.count_rhyme, 3)
        if self.intern_rhyme_score != 0:
            self.intern_rhyme_score = round(self.intern_rhyme_score / self.count, 3)
        if self.consonant_rhyme_score != 0:
            self.consonant_rhyme_score = round(self.consonant_rhyme_score / self.count_rhyme, 3)
        if self.score_result != 0:
            self.score_result = round(self.score_result / self.count, 3)