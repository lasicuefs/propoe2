import random
from .score import Score
from collections import Counter
from .poem_evaluation import Evaluation


class Poem_builder():

    def __init__(self, sentences, metrics, rhyme, score_weight, seed):
        self.sentences = sentences
        self.rhyme = rhyme
        self.metrics = metrics
        self.poem = ""
        self.verse_list = {}
        self.score_weight = score_weight
        self.evaluation = Evaluation()
        random.seed(seed)

    def result(self):
        print(self.poem)
        print(self.evaluation)

    def save(self, path):
        text_file = open(path, "w")
        text_file.write(self.poem)
        text_file.close()

    def build(self, verbose=False):
        sentences = self.get_poem_sentences(verbose)
        self.verse_list = sentences.copy()
        for letter in self.rhyme:
            if letter == " ":
                self.poem = self.poem + "\n"
            else:
                s = sentences[letter].pop(0)
                self.poem = self.poem + s.sentence + "\n"

    def random_sentence(self, letter, sentences, metric_count):
        pos_sentences = self.sentences[letter].metrics[self.metrics[metric_count]]
        number = random.randrange(len(pos_sentences))
        s = pos_sentences[number]
        if s.not_in(sentences[letter]):
            return s
        else:
            return self.random_sentence(letter, sentences, metric_count)

    def random_verse(self, sentence):
        number = random.randrange(len(sentence.verse_structures))
        return sentence.verse_structures[number]

    def initialize_sentences(self):
        sentences = {}
        for letter in self.sentences:
            sentences[letter] = []
        return sentences

    def get_poem_sentences(self, verbose):
        rhyme = self.rhyme
        sentences = self.initialize_sentences()
        last_rhyme = {}
        new_strophe = True
        metric_count = 0
        for letter in rhyme:
            if letter == " ":
                new_strophe = True
            elif new_strophe:
                current = self.random_sentence(letter, sentences, metric_count)
                sentences[letter].append(current)
                current_verse = self.random_verse(current)
                fixed_verse = current_verse
                last_rhyme[letter] = current_verse
                if verbose:
                    print(current_verse.scanned_sentence)
                    print()
                new_strophe = False
                metric_count += 1
            else:
                if letter in last_rhyme:
                    verse_rhyme = last_rhyme[letter]
                else:
                    verse_rhyme = None
                next_s, next_verse = self.find_sentence(
                    sentences, [current_verse, fixed_verse], letter,
                    verse_rhyme, metric_count, verbose)

                last_rhyme[letter] = next_verse
                sentences[letter].append(next_s)
                current = next_s
                current_verse = next_verse
                metric_count += 1

        return sentences

    def find_sentence(self, sentences, verses, letter, last_rhyme, metric_count, verbose):
        max_score = -1
        for sentence in self.sentences[letter].metrics[self.metrics[metric_count]]:
            if sentence.not_in(sentences[letter]):
                for possible_verse in sentence.verse_structures:
                    # Use two verses as reference
                    # And sum the scores
                    score = Score(possible_verse.scanned_sentence)
                    for verse in verses:
                        score.score(verse, possible_verse,
                                    last_rhyme, self.score_weight)
                        if score.score_result > max_score:
                            max_score = score.score_result
                            next_s = sentence
                            next_verse = possible_verse
                            result_score = score
        if verbose:
            print(result_score)
            print()

        self.evaluation.add(result_score)
        return next_s, next_verse
