from src.model.semantic.metaphor import Metaphor
from src.model.semantic.semanticSimilarity import SemanticSimilarity
from src.model.sentence import Sentence
from src.model.verse_structure import VerseStructure


class Score:
    def __init__(self):
        self.consonant_rhyme_score = 0
        self.accent_score = 0
        self.stress_score = 0
        self.rhyme_verse: bool = False
        self.rhyme_structure_score = 0
        self.score_result = 0
        self.rhyme_intern_score = 0
        self.semantic_similarity = 0
        self.metaphor = 0

class VerseScore:
    def __init__(self, verse, model) -> None:
        # TODO: What is ``verse``'s type?
        # TODO: Are all those scores integers or floats?
        self.semanticSimilarity = SemanticSimilarity()
        self.metaphor = Metaphor()
        self.model = model
        self.verse = verse  # Scanned Verse
        self.score = Score()
        self.debug_repr: dict[str, str] = {
            "Rima Consoante": "",
            "Estrutura Ritmica": "",
            "Silabas Tonicas": "",
            "Acento": "",
            "Rima Interna": "",
            "Similaridade Semantica": "",
            "Resultado": "",
        }

    def __repr__(self) -> str:
        output = "Verso: " + self.verse + "\n Scores:"
        if self.debug_repr["Rima Consoante"] == "":
            output = output + "\n - Rima Consoante: Sem verso que rima"
        else:
            output = (
                    output
                    + "\n - Rima Consoante: "
                    + str(round(self.score.consonant_rhyme_score, 3))
                    + self.debug_repr["Rima Consoante"]
            )

        output = (
            output
            + "\n - Estrutura Ritmica: "
            + str(round(self.score.rhyme_structure_score, 3))
            + self.debug_repr["Estrutura Ritmica"]
        )

        output = (
            output
            + "\n - Silabas Tônicas: "
            + str(round(self.score.stress_score, 3))
            + self.debug_repr["Silabas Tonicas"]
        )
        if self.debug_repr["Rima Consoante"] == "":
            output = output + "\n - Acento: Sem verso que rima"
        else:
            output = (
                    output
                    + "\n - Acento: "
                    + str(round(self.score.accent_score, 3))
                    + self.debug_repr["Acento"]
            )

        output = (
            output
            + "\n - Rima Interna: "
            + str(round(self.score.rhyme_intern_score, 3))
            + self.debug_repr["Rima Interna"]
        )

        output = (
                output
                + "\n - Similaridade Semântica: "
                + str(round(self.score.semantic_similarity, 3))
                + self.debug_repr["Similaridade Semantica"]
        )
        output = (
                output
                + "\n - Metáfora: "
                + str(round(self.score.metaphor, 3))
        )

        output = (
            output
            + "\n - Score Resultante: "
            + str(round(self.score.score_result, 3))
            + self.debug_repr["Resultado"]
        )

        return output

    def jacard(self, a, b) -> tuple[float, str]:
        # TODO: What are ``a`` and ``b``?
        a = set(a)
        b = set(b)
        n_intersect = len(set.intersection(a, b))
        d = "\nIntercessão: " + str(set.intersection(a, b))
        n_union = len(set.union(a, b))
        d += "\nUnião: " + str(set.union(a, b))
        d += "\nJaccard: " + str(n_intersect / n_union)
        return n_intersect / n_union, d

    def intern_rhyme(self, a: VerseStructure) -> float:
        self.debug_repr["Rima Interna"] = ""
        syllables = a.get_syllables()
        self.debug_repr["Rima Interna"] += (
            "\nSílabas: "
            + str(syllables)
            + "\nSílabas únicas: "
            + str(set(syllables))
            + "\nQuantidade de sílabas: "
            + str(len(syllables))
            + "\nQuantidade de sílabas únicas: "
            + str(len(set(syllables)))
        )
        return 1 - (len(set(syllables)) / len(syllables))

    def same_stress_pos(self, a: VerseStructure, b: VerseStructure) -> float:
        """Score rhyme structure."""
        self.debug_repr["Estrutura Ritmica"] += (
            "\nPosição das sílabas acentuadas:"
            + "\nReferência: "
            + str(a.stress_position)
            + "\nSegmento: "
            + str(b.stress_position)
        )

        result, d = self.jacard(a.stress_position, b.stress_position)
        self.debug_repr["Estrutura Ritmica"] += d
        return result

    def same_stress_syllable(self, a: VerseStructure, b: VerseStructure) -> float:
        """Score similar stress syllables.

        It is multiplied by 0.5 because this score is half the score for stress syllables.
        """
        count = 0
        for s in a.stress_syllables:
            if s in b.stress_syllables:
                count += 1
        div = self.get_size(a.stress_syllables, b.stress_syllables)
        result = count / div
        self.debug_repr["Silabas Tonicas"] += (
            "\nSílabas acentuadas:"
            + "\nReferência: "
            + str(a.stress_syllables)
            + "\nSegmento: "
            + str(b.stress_syllables)
            + "\nResultado: "
            + str(result)
        )

        return result * 0.5

    def same_pos_stress_syllable(self, a: VerseStructure, b: VerseStructure) -> float:
        """Score stress syllables at same position.

        It is multiplied by 0.5 because this score is half the score for stress syllables.
        """
        a_stress = set(a.stress_position)
        b_stress = set(b.stress_position)
        div = self.get_size(a_stress, b_stress)
        intersect = set.intersection(a_stress, b_stress)
        score = 0

        self.debug_repr["Silabas Tonicas"] += (
            "\nScore da posição igual:"
            + "\nDividendo: "
            + str(div)
            + "\nIntercessão: "
            + str(intersect)
        )

        for pos in intersect:
            self.debug_repr["Silabas Tonicas"] += (
                "\nReferência: "
                + str(a.pos_stress_dict[pos])
                + ", posição = "
                + str(pos)
                + "\nSegmento: "
                + str(b.pos_stress_dict[pos])
                + ", posição = "
                + str(pos)
            )
            if a.pos_stress_dict[pos] == b.pos_stress_dict[pos]:
                score += 1
        self.debug_repr["Silabas Tonicas"] += "\n Resultado: " + str(score / div)

        return score / div * 0.5

    def get_size(self, a, b) -> int:
        len_a = len(a)
        len_b = len(b)
        if len_a > len_b:
            return len_b
        else:
            return len_a

    def same_accent(self, a: VerseStructure, b: VerseStructure) -> bool:
        # TODO: verify is ``a`` and ``b`` types are right, I'm guessing it's ``VerseStructure``
        self.debug_repr["Acento"] = ""
        self.debug_repr["Acento"] += (
            "\nAcento da referência: "
            + str(a.accent)
            + "\nAcento do segmento: "
            + str(b.accent)
        )
        return a.accent == b.accent

    def consonant_rhyme(self, a: VerseStructure, b: VerseStructure) -> float:
        a_stress = a.get_last_syllables()
        b_stress = b.get_last_syllables()
        self.debug_repr["Rima Consoante"] = (
            "\nLetras após vogal acentuada: \n"
            + "Referência: "
            + a_stress
            + "\n"
            + "Segmento: "
            + b_stress
        )
        if a_stress == b_stress:
            self.debug_repr["Rima Consoante"] += "\n" + a_stress + " = " + b_stress
            return 1
        elif a_stress[0] == b_stress[0]:
            self.debug_repr["Rima Consoante"] += (
                "\n" + a_stress[0] + " = " + b_stress[0]
            )
            return 0.5
        else:
            self.debug_repr["Rima Consoante"] += (
                "\n" + a_stress[0] + " != " + b_stress[0]
            )
            return 0

    def score_calculation(self, ref_verse, possible_verse, rhyme_verse, weight, last_verse:Sentence) -> None:
        """Calculates the score.

                Parameters:
                  ref_verse: First strophe verse.
                  last_verse: Last verser choosed
                  possible_verse: Structure of new possible verse.
                  rhyme_verse: Last verse that have the same rhyme.
                  weight: Weight of each parameter of score.
                """
        self.score.rhyme_structure_score = (self.same_stress_pos(ref_verse, possible_verse) + self.same_stress_pos(last_verse.verse_structures[0], possible_verse))/2
        self.score.intern_rhyme_score = self.intern_rhyme(possible_verse)
        s = self.same_stress_syllable(ref_verse, possible_verse) + self.same_stress_syllable(last_verse.verse_structures[0], possible_verse)
        ps = self.same_pos_stress_syllable(ref_verse, possible_verse) + self.same_pos_stress_syllable(last_verse.verse_structures[0], possible_verse)
        self.score.stress_score = (s + ps) / 2
        self.rhyme_verse = rhyme_verse
        self.score.semantic_similarity = (self.semanticSimilarity.cossineSimilarity(possible_verse.sentence, last_verse.sentence, self.model)
        + self.semanticSimilarity.cossineSimilarity(possible_verse.sentence, ref_verse.sentence, self.model))/2

        self.debug_repr["Similaridade Semantica"] += (
                "\nVerso de referência: "
                + f"{ref_verse.sentence}"
                + "\nSentenca Anterior: "
                + f"{last_verse.sentence}"
        )
        self.score.metaphor = self.metaphor.metaphor_degree(possible_verse.sentence)

        if rhyme_verse:
            self.score.accent_score = self.same_accent(possible_verse, rhyme_verse)
            self.score.consonant_rhyme_score = self.consonant_rhyme(possible_verse, rhyme_verse)

        self.score.score_result = (
            self.score.rhyme_structure_score * weight["Estrutura ritmica"]
            + self.score.stress_score * weight["Posicao tonica"]
            + self.score.accent_score * weight["Acentuacao"]
            + self.score.consonant_rhyme_score * weight["Rima toante & consoante"]
            + self.score.intern_rhyme_score * weight["Rima interna"]
            + self.score.semantic_similarity * weight["Similaridade Semântica"]
            + self.score.metaphor * weight["Metafora"]
        )

        max_score = (
            weight["Estrutura ritmica"]
            + weight["Posicao tonica"]
            + weight["Rima interna"]
            + weight["Similaridade Semântica"]
            + weight["Metafora"]
        )
        self.debug_repr["Resultado"] = ""
        self.debug_repr["Resultado"] += "\nSoma dos critérios: " + str(
            round(self.score.score_result, 2)
        )
        if rhyme_verse:
            max_score += weight["Rima toante & consoante"] + weight["Acentuacao"]
            self.debug_repr["Resultado"] += "\nScore máximo: " + str(max_score)
        else:
            self.debug_repr["Resultado"] += "\nScore máximo: " + str(max_score)
        self.score.score_result = self.score.score_result / max_score


class PoemScore:

    def __init__(self, verseScoreList:list):
        self.score = Score()
        self.extractPoemScoreFromVerseScore(verseScoreList)

    def extractPoemScoreFromVerseScore(self, verseScoreList:list):
        verse_rhyme_num = 0
        count_verses = 0
        for verseScore in verseScoreList:
            if verseScore != None:
                self.score.consonant_rhyme_score += verseScore.score.consonant_rhyme_score
                self.score.accent_score += verseScore.score.accent_score
                self.score.stress_score += verseScore.score.stress_score
                self.score.rhyme_structure_score += verseScore.score.rhyme_structure_score
                self.score.score_result += verseScore.score.score_result
                self.score.rhyme_intern_score += verseScore.score.intern_rhyme_score
                self.score.semantic_similarity += verseScore.score.semantic_similarity
                self.score.metaphor += verseScore.score.metaphor
                if verseScore.rhyme_verse:
                    verse_rhyme_num += 1
                count_verses+=1

        self.calculatePoemScore(count_verses, verse_rhyme_num)

    def calculatePoemScore(self, verses_num, verse_rhyme_num):
        if self.score.consonant_rhyme_score != 0:
            self.score.consonant_rhyme_score = round(self.score.consonant_rhyme_score / verse_rhyme_num, 3)
        if self.score.accent_score != 0:
            self.score.accent_score = round(self.score.accent_score / verse_rhyme_num, 3)
        if self.score.stress_score != 0:
            self.score.stress_score = round(self.score.stress_score / verses_num, 3)
        if self.score.rhyme_structure_score != 0:
            self.score.rhyme_structure_score = round(self.score.rhyme_structure_score / verses_num, 3)
        if self.score.rhyme_intern_score != 0:
            self.score.rhyme_intern_score = round(self.score.rhyme_intern_score / verses_num, 3)
        if self.score.semantic_similarity != 0:
            self.score.semantic_similarity = round(self.score.semantic_similarity / verses_num, 3)
        if self.score.metaphor != 0:
            self.score.metaphor = round(self.score.metaphor / verses_num, 3)
        if self.score.score_result != 0:
            self.score.score_result = round(self.score.score_result / verses_num, 3)

    def __repr__(self) -> str:
        return (
            "Resultado:"
            + "\n - Estrutura Ritmica: "
            + str(self.score.rhyme_structure_score)
            + "\n - Silabas Tônicas: "
            + str(self.score.stress_score)
            + "\n - Acento: "
            + str(self.score.accent_score)
            + "\n - Rima Interna: "
            + str(self.score.rhyme_intern_score)
            + "\n - Rima Toante & Consoante: "
            + str(self.score.consonant_rhyme_score)
            + "\n - Similaridade Semântica "
            + str(self.score.semantic_similarity)
            + "\n - Metáfora: "
            + str(self.score.metaphor)
            + "\n Score Resultante: "
            + str(self.score.score_result)
        )