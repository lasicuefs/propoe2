import re


class Verse_structure():

    def __init__(self, syllable_number, stress_position, scanned_sentence):
        self.syllable_number = syllable_number
        self.stress_position = stress_position.split()
        self.scanned_sentence = scanned_sentence
        self.stress_syllables = self.stress_syllable()
        self.accent = self.accentuation()

    def __repr__(self):
        return ("\n Syllable number: " + str(self.syllable_number) +
                "\n Stress position: " + " ".join(self.stress_position) +
                "\n Scanned sentence: " + self.scanned_sentence +
                "\n Stress syllables: " + str(self.stress_syllables) +
                "\n Accentuation: " + str(self.accent))

    def stress_syllable(self):
        syllables = []
        splited_sentence = self.scanned_sentence.split('/')
        for pos in self.stress_position:
            syllables.append(splited_sentence[int(pos) - 1])
        return syllables

    def remove_end_ponctuation(self, sentence):
        return re.sub('^[^a-zA-Z]*|[^a-zA-Z]*$', '', sentence)

    def accentuation(self):
        s = self.remove_end_ponctuation(self.scanned_sentence)
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
