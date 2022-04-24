import random
from .score import Score
from collections import Counter
from .poem_evaluation import Evaluation


class Poem_builder():

    def __init__(self, sentences, metrics, rhyme, score_weight, seed):
        # List of Rhyme objects
        self.sentences = sentences
        # Ex: "AABB CCDD"
        self.rhyme = rhyme
        # List of metrics per verse
        self.metrics = metrics
        self.poem = ""
        # Dict that maps score name and its weight
        self.score_weight = score_weight
        self.evaluation = Evaluation()
        random.seed(seed)

    def result(self):
        print(self.poem)
        print(self.evaluation)

    def save(self, path):
        """ Save poem in txt file.
        """
        text_file = open(path, "w")
        text_file.write(self.poem)
        text_file.close()

    def build(self, verbose=False):
        """ Build poem. Get best sentences and add it in the string self.poem.

        Parameter:
          verbose: If True, prints the score os every sentence in the poem.
        """
        sentences = self.get_poem_sentences(verbose)
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
        """ Initializa a Dict mapping the letters from the rhyme pattern to an empty list.
        """
        sentences = {}
        for letter in self.sentences:
            sentences[letter] = []
        return sentences

    def get_poem_sentences(self, verbose):
        """ Return a list of Sentence objects in order to build a poem.
        """
        rhyme = self.rhyme
        sentences = self.initialize_sentences()
        # Dict that maps letters from rhyme pattern to its last Rhyme object
        last_rhyme = {}
        new_strophe = True
        # Index from self.metrics that shows with metric does this Sentence object needs.
        metric_count = 0
        # Iterate through every letter from rhyme pattern, one by one, in order.
        for letter in rhyme:
            if letter == " ":
                new_strophe = True
            elif new_strophe:
                current = self.random_sentence(letter, sentences, metric_count)
                sentences[letter].append(current)
                current_verse = self.random_verse(current)
                # Reference verse.
                fixed_verse = current_verse
                last_rhyme[letter] = current_verse
                if verbose:
                    print(current_verse.scanned_sentence)
                    print()
                new_strophe = False
                metric_count += 1
            else:
                # If not a new rhyme, if there is a verse we can compare to.
                if letter in last_rhyme:
                    # Last Verse object that rhymes with the new verse to be found.
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
        """ Return best Sentence object given a score.

        Parameters:
          sentences: List of Sentence objects chosen for the current poem. 
          verses: List with only the first Verse object of strophe and the current Verse object.
          letter: Which rhyme pattern it is. EX: "A", "B" or "C".
          last_rhyme: Verse object of the last Sentence that rhymes.
          metric_count: Index from self.metrics that shows with metric does 
            this Sentence object needs.
          verbose: If True, prints the chosen sentence and its scores.

        Return:
          next_s: Chosen Sentence object
          next_verse: Chosen Verse object from the Sentence object
        """
        max_score = -1
        for sentence in self.sentences[letter].metrics[self.metrics[metric_count]]:
            if sentence.not_in(sentences[letter]):
                for possible_verse in sentence.verse_structures:
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
