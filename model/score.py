from .utils import consonant_removal


class Score():

    def __init__(self, verse):
        self.verse = verse  # Scanned Verse
        self.consonant_rhyme_score = 0
        self.accent_score = 0
        self.stress_score = 0
        self.rhyme_structure_score = 0
        self.score_result = 0
        self.rhyme_intern_score = 0
        self.toante_rhyme_score = 0

    def __repr__(self):

        return ("Verso: " + self.verse +
                "\n Scores:" +
                "\n - Rima Consoante: " + str(round(self.consonant_rhyme_score, 2)) +
                "\n - Estrutura Ritmica: " + str(round(self.rhyme_structure_score, 2)) +
                "\n - Silabas Tônicas: " + str(round(self.stress_score, 2)) +
                "\n - Acento: " + str(round(self.accent_score, 2)) +
                "\n - Rima Interna: " + str(round(self.intern_rhyme_score, 2)) +
                "\n - Rima Toante: " + str(round(self.toante_rhyme_score, 2)) +
                "\n Score Resultante: " + str(round(self.score_result, 2)))

    def jacard(self, a, b):
        a = set(a)
        b = set(b)
        n_intersect = len(set.intersection(a, b))
        n_union = len(set.union(a, b))
        return n_intersect/n_union

    def intern_rhyme(self, a):
        syllables = a.get_syllables()
        return 1 - (len(set(syllables))/len(syllables))

    def same_stress_pos(self, a, b):
        """ Score rhyme structure.
        """
        return self.jacard(a.stress_position, b.stress_position)

    def same_stress_syllable(self, a, b):
        """ Score similar stress syllables.

        It is multiplied by 0.5 because this score is half the score for stress syllables.
        """
        return self.jacard(a.stress_syllables, b.stress_syllables) * 0.5

    def same_pos_stress_syllable(self, a, b):
        """ Score stress syllables at same position.

        It is multiplied by 0.5 because this score is half the score for stress syllables.
        """
        a_stress = set(a.stress_position)
        b_stress = set(b.stress_position)
        div = self.get_size(a_stress, b_stress)
        intersect = set.intersection(a_stress, b_stress)
        score = 0
        for pos in intersect:
            if a.pos_stress_dict[pos] == b.pos_stress_dict[pos]:
                score += 1
        return score/div * 0.5

    def get_size(self, a, b):
        len_a = len(a)
        len_b = len(b)
        if len_a > len_b:
            return len_b
        else:
            return len_a

    def same_accent(self, a, b):
        return a.accent == b.accent

    def consonant_rhyme(self, a, b):
        a_word = a.get_last_word().strip()
        b_word = b.get_last_word().strip()
        size = self.get_size(a_word, b_word)
        count = 0
        for i in range(size):
            if a_word[-(i+1)] == b_word[-(i+1)]:
                count += 1
        return count/size

    def toante_rhyme(self, a, b):
        a_stress = consonant_removal(a.get_last_stress())
        b_stress = consonant_removal(b.get_last_stress())
        return a_stress == b_stress

    def score(self, reference, possible_verse, rhyme_verse, weight):
        self.rhyme_structure_score += self.same_stress_pos(
            reference, possible_verse)
        self.intern_rhyme_score = self.intern_rhyme(possible_verse)
        s = self.same_stress_syllable(reference, possible_verse)
        ps = self.same_pos_stress_syllable(reference, possible_verse)
        self.stress_score += s + ps  # Sum to one max
        if rhyme_verse:
            self.accent_score += self.same_accent(possible_verse, rhyme_verse)
            self.consonant_rhyme_score += self.consonant_rhyme(
                possible_verse, rhyme_verse)
            self.toante_rhyme_score += self.toante_rhyme(
                possible_verse, rhyme_verse)

        self.score_result = self.rhyme_structure_score * weight["Estrutura ritmica"] + \
            self.stress_score * weight["Posicao tonica"] + \
            self.accent_score * weight["Acentuacao"] + \
            self.consonant_rhyme_score * weight["Rima consoante"] + \
            self.intern_rhyme_score * weight["Rima interna"] + \
            self.toante_rhyme_score * weight["Rima toante"]
