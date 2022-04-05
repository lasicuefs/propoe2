import random
from .score import score
from collections import Counter
import numpy as np
from .accent import *


class Poem_builder():

    def __init__(self, sentences, chosen_rhymes, rhyme):
        self.sentences = sentences
        self.rhyme = rhyme
        self.chosen_rhymes = chosen_rhymes
        self.poem = ""
        self.verse_list = {}

    def build(self):
        sentences = self.get_poem_sentences()
        self.verse_list = sentences.copy()
        for letter in self.rhyme:
            if letter == " ":
                self.poem = self.poem + "\n"
            else:
                s = sentences[letter].pop(0)
                self.poem = self.poem + s.sentence + "\n"

    def random_sentence(self, letter):
        number = random.randrange(
            len(self.sentences[self.chosen_rhymes[letter]]))
        return self.sentences[self.chosen_rhymes[letter]][number]

    def random_verse(self, sentence):
        number = random.randrange(len(sentence.verse_structures))
        return sentence.verse_structures[number]

    def initialize_accent_vector(self):
        last_accent = {}
        for letter in self.chosen_rhymes:
            last_accent[letter] = [0, 0, 0]
        return last_accent

    def initialize_sentences(self):
        sentences = {}
        for letter in self.chosen_rhymes:
            sentences[letter] = []
        return sentences

    def get_poem_sentences(self):
        rhyme = self.rhyme
        sentences = self.initialize_sentences()
        last_accent = self.initialize_accent_vector()
        skip = True
        for letter in rhyme:
            if letter == " ":
                skip = True
            elif skip:
                current = self.random_sentence(letter)
                sentences[letter].append(current)
                pos = accent_pos(current.verse_structures[0].accent)
                last_accent[letter][pos] += 1
                current_verse = self.random_verse(current)
                skip = False
            else:
                next_s, next_verse = self.find_sentence(
                    sentences, current_verse, letter,
                    self.chosen_rhymes[letter],
                    next_accent(last_accent[letter]))

                pos = accent_pos(next_verse.accent)
                last_accent[letter][pos] += 1
                sentences[letter].append(next_s)
                current = next_s
                current_verse = next_verse

        return sentences

    def find_sentence(self, sentences, verse, letter, rhyme, last_accent):
        max_score = -1

        for sentence in self.sentences[rhyme]:
            if sentence.not_in(sentences[letter]):
                for possible_verse in sentence.verse_structures:
                    pos_score = score(
                        verse, possible_verse, last_accent)
                    if pos_score > max_score:
                        max_score = pos_score
                        next_s = sentence
                        next_verse = possible_verse

        return next_s, next_verse
