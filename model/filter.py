from collections import Counter
import random


class Filter():
    def __init__(self, sentences):
        self.sentences = sentences
        self.rhyme_count = self.rhyme_counter()

    def rhyme_counter(self):
        rhyme_count = {}
        for key in self.sentences.keys():
            length = len(set(self.sentences[key]))
            if length not in rhyme_count:
                rhyme_count[length] = []
            rhyme_count[length].append(key)
        return rhyme_count

    def get_rhymes(self, minimun):
        rhymes = []
        for key in self.rhyme_count.keys():
            if int(key) > minimun:
                rhymes.extend(self.rhyme_count[key])
        return rhymes

    def random_rhyme(self, rhymes):
        number = random.randrange(len(rhymes))
        return rhymes[number]

    def rhyme_filter(self, rhyme):
        rhyme = self.remove_space(rhyme)
        rhymes_struct = Counter(rhyme)
        filtered_rhymes = {}
        for letter in rhymes_struct:
            rhymes = self.get_rhymes(rhymes_struct[letter])
            r = self.random_rhyme(rhymes)
            filtered_rhymes[letter] = r
        return filtered_rhymes

    def remove_space(self, rhyme):
        return rhyme.replace(" ", "")
