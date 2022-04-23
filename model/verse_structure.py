import re
from .utils import *


class Verse_structure():

    def __init__(self, sentence, syllable_number, stress_position, scanned_sentence):
        self.metric = int(syllable_number)
        self.stress_position = stress_position.split()
        self.scanned_sentence = scanned_sentence
        self.stress_syllables, self.pos_stress_dict = self.stress_syllable()
        self.accent = self.accentuation()
        self.syllables = self.get_syllables()
        self.sentence = sentence

    def __repr__(self):
        return ("\n Syllable number: " + str(self.metric) +
                "\n Stress position: " + " ".join(self.stress_position) +
                "\n Scanned sentence: " + self.scanned_sentence +
                "\n Stress syllables: " + str(self.stress_syllables) +
                "\n Accentuation: " + str(self.accent))

    def get_syllables(self):
        sentence = scanned_sentence_preprocess(self.scanned_sentence)
        return [s.strip() for s in sentence.split("/")]

    def get_last_word(self):
        sentence = remove_end_ponctuation(self.sentence)
        word = sentence.split(" ")[-1]
        return word

    def get_last_stress(self):
        print(self.scanned_sentence)
        print(self.stress_syllables[-1])

    def stress_syllable(self):
        syllables = []
        pos_syllables = {}
        splited_sentence = self.scanned_sentence.split('/')
        for pos in self.stress_position:
            s = splited_sentence[int(pos) - 1]
            syllables.append(s.strip())
            pos_syllables[pos] = s.strip()
        return syllables, pos_syllables

    def accentuation(self):
        s = remove_end_ponctuation(self.scanned_sentence)
        last_word = s.split()[-1]
        syllables = last_word.split('/')
        for i in range(1, len(syllables) + 1):
            if '#' in syllables[-i]:
                if i == 3:
                    return 'Esdrúxula'
                elif i == 2:
                    return 'Grave'
                elif i == 1:
                    return 'Aguda'
