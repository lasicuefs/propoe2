import re
from .utils import *


class Sentence ():

    def __init__(self, sentence, link, sentence_number, verse_structures):
        self.sentence = sentence
        self.sentence_clean = remove_end_ponctuation(sentence)
        self.link = link
        self.sentence_number = sentence_number
        self.verse_structures = verse_structures

    def __eq__(self, other):
        sentence = sentence_preprocess(self.sentence_clean)
        other = sentence_preprocess(other.sentence_clean)
        return sentence.split()[-1].strip() == other.split()[-1].strip()

    def __hash__(self):
        return hash(('sentence', self.sentence_clean))

    def __repr__(self):
        verses_repr = "\n".join([verse.__repr__()
                                for verse in self.verse_structures])
        return ("\n\n Sentence: " + self.sentence +
                "\n link: " + str(self.link) +
                "\n sentence number: " + str(self.sentence_number) +
                "\n Verses: " + verses_repr)

    def not_in(self, sentences):
        for sentence in sentences:
            if self.__eq__(sentence):
                return False
        return True

    def get_metric(self, m):
        verses = []
        for verse in self.verse_structures:
            if verse.metric == m:
                verses.append(verse)
        return Sentence(self.sentence, self.link, self.sentence_number, verses)
