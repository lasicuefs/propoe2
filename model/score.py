from .utils import consonant_removal


class Score():

    def __init__(self, verse):
        self.verse = verse  # Scanned Verse
        self.accent_score = 0
        self.stress_score = 0
        self.rhyme_structure_score = 0
        self.score_result = 0
        self.rhyme_verse = False
        self.debug_repr = {
            "Estrutura Ritmica": "",
            "Silabas Tonicas": "",
            "Acento": "",
            "Resultado": ""
        }

    def __repr__(self):
        output = "Verso: " + self.verse + "\n Scores:"

        output = output + "\n - Estrutura Ritmica: " + str(round(self.rhyme_structure_score, 3)) + \
            self.debug_repr["Estrutura Ritmica"]

        output = output + "\n - Silabas Tônicas: " + str(round(self.stress_score, 3)) + \
            self.debug_repr["Silabas Tonicas"]

        output = output + "\n - Acento: " + str(round(self.accent_score, 3)) + \
            self.debug_repr["Acento"]

        output = output + "\n - Score Resultante: " + str(round(self.score_result, 3)) + \
            self.debug_repr["Resultado"]

        return output

    def jacard(self, a, b):
        a = set(a)
        b = set(b)
        n_intersect = len(set.intersection(a, b))
        d = "\nIntercessão: " + str(set.intersection(a, b))
        n_union = len(set.union(a, b))
        d += "\nUnião: " + str(set.union(a, b))
        d += "\nJaccard: " + str(n_intersect/n_union)
        return n_intersect/n_union, d

    # def intern_rhyme(self, a):
    #     self.debug_repr["Rima Interna"] = ""
    #     syllables = a.get_syllables()
    #     self.debug_repr["Rima Interna"] += "\nSílabas: " + str(syllables) + \
    #         "\nSílabas únicas: " + str(set(syllables)) + \
    #         "\nQuantidade de sílabas: " + str(len(syllables)) + \
    #         "\nQuantidade de sílabas únicas: " + str(len(set(syllables)))
    #     return 1 - (len(set(syllables))/len(syllables))

    def same_stress_pos(self, a, b):
        """ Score rhyme structure.
        """
        self.debug_repr["Estrutura Ritmica"] += "\nPosição das sílabas acentuadas:" + \
            "\nReferência: " + str(a.stress_position) + \
            "\nSegmento: " + str(b.stress_position)

        result, d = self.jacard(a.stress_position, b.stress_position)
        self.debug_repr["Estrutura Ritmica"] += d
        return result

    def same_stress_syllable(self, a, b):
        """ Score similar stress syllables.

        It is multiplied by 0.5 because this score is half the score for stress syllables.
        """
        count = 0
        for s in a.stress_syllables:
            if s in b.stress_syllables:
                count += 1
        div = self.get_size(a.stress_syllables, b.stress_syllables)
        result = count/div
        self.debug_repr["Silabas Tonicas"] += "\nSílabas acentuadas:" +\
            "\nReferência: " + str(a.stress_syllables) + \
            "\nSegmento: " + str(b.stress_syllables) + \
            "\nResultado: " + str(result)

        return result * 0.5

    def same_pos_stress_syllable(self, a, b):
        """ Score stress syllables at same position.

        It is multiplied by 0.5 because this score is half the score for stress syllables.
        """
        a_stress = set(a.stress_position)
        b_stress = set(b.stress_position)
        div = self.get_size(a_stress, b_stress)
        intersect = set.intersection(a_stress, b_stress)
        score = 0

        self.debug_repr["Silabas Tonicas"] += "\nScore da posição igual:" +\
            "\nDividendo: " + str(div) +\
            "\nIntercessão: " + str(intersect)

        for pos in intersect:
            self.debug_repr["Silabas Tonicas"] += "\nReferência: " + str(a.pos_stress_dict[pos]) + \
                ", posição = " + str(pos) + \
                "\nSegmento: " + str(b.pos_stress_dict[pos]) + \
                ", posição = " + str(pos)
            if a.pos_stress_dict[pos] == b.pos_stress_dict[pos]:
                score += 1
        self.debug_repr["Silabas Tonicas"] += "\n Resultado: " + str(score/div)

        return score/div * 0.5

    def get_size(self, a, b):
        len_a = len(a)
        len_b = len(b)
        if len_a > len_b:
            return len_b
        else:
            return len_a

    def same_accent(self, a, b):
        self.debug_repr["Acento"] = ""
        self.debug_repr["Acento"] += "\nAcento da referência: " + str(a.accent) +\
            "\nAcento do segmento: " + str(b.accent)
        return a.accent == b.accent

    def consonant_rhyme(self, a, b):
        a_stress = a.get_last_syllables()
        b_stress = b.get_last_syllables()
        self.debug_repr["Rima Consoante"] = "\nLetras após vogal acentuada: \n" + \
                                            "Referência: " + a_stress + "\n" + \
                                            "Segmento: " + b_stress
        if(a_stress == b_stress):
            self.debug_repr["Rima Consoante"] += "\n" + \
                a_stress + " = " + b_stress
            return 1
        elif(a_stress[0] == b_stress[0]):
            self.debug_repr["Rima Consoante"] += "\n" + a_stress[0] + \
                " = " + b_stress[0]
            return 0.5
        else:
            self.debug_repr["Rima Consoante"] += "\n" + a_stress[0] + \
                " != " + b_stress[0]
            return 0

    def score(self, reference, possible_verse, rhyme_verse, weight):
        self.rhyme_structure_score += self.same_stress_pos(
            reference, possible_verse)/2
        # self.intern_rhyme_score = self.intern_rhyme(possible_verse)
        # s = self.same_stress_syllable(reference, possible_verse)
        ps = self.same_pos_stress_syllable(reference, possible_verse)
        # self.stress_score += (s + ps)/2
        self.stress_score += ps
        self.rhyme_verse = rhyme_verse
        if rhyme_verse:
            self.accent_score = self.same_accent(possible_verse, rhyme_verse)
            # self.consonant_rhyme_score = self.consonant_rhyme(
            #     possible_verse, rhyme_verse)

        self.score_result = self.rhyme_structure_score * weight["Estrutura ritmica"] + \
            self.stress_score * weight["Posicao tonica"] + \
            self.accent_score * weight["Acentuacao"]

        max_score = weight["Estrutura ritmica"] + \
            weight["Posicao tonica"]
        self.debug_repr["Resultado"] = ""
        self.debug_repr["Resultado"] += "\nSoma dos critérios: " + \
            str(round(self.score_result, 2))
        if rhyme_verse:
            max_score += weight["Acentuacao"]
            self.debug_repr["Resultado"] += "\nScore máximo: " + \
                str(max_score)
            self.score_result = self.score_result/max_score
        else:
            self.debug_repr["Resultado"] += "\nScore máximo: " + \
                str(max_score)
            self.score_result = self.score_result/max_score
