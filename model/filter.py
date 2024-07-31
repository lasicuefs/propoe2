from collections import Counter
import random
from .utils import remove_space


class Filter():
    def __init__(self, sentences, metric, rhyme_pattern, seed):
        # List of Rhyme objects
        self.sentences = sentences
        # List of metrics for each verse
        self.metric = metric
        # String with letters representing rhyme. EX: "AABB CCDD"
        self.rhyme = remove_space(rhyme_pattern)
        # List of Rhyme objects
        self.chosen_rhymes = []
        random.seed(seed)

    def get_rhymes(self):
        """ Return which Rhyme objects to use for each letter in the rhyme pattern.

        Return:
          sentences: Dict of letters from rhyme pattern that maps to a Rhyme object
            EX: {"A": Rhyme, "B": Rhyme}

        """
        rhymes = self.rhyme_filter()
        sentences = {}
        for letter in rhymes:
            sentences[letter] = self.random_rhyme(rhymes[letter])
        return sentences
        # sentences['A'] = self.sentences[116]
        # sentences['B'] = self.sentences[39]
        # return sentences


    def random_rhyme(self, rhymes):
        """ Return a random Rhyme object inside a list of Rhyme objects
        """
        number = random.randrange(len(rhymes))
        rhyme = rhymes[number]
        if rhyme.not_in(self.chosen_rhymes):
            self.chosen_rhymes.append(rhyme)
            return rhyme
        else:
            return self.random_rhyme(rhymes)

    def rhyme_filter(self):
        """Filter Rhyme object inside self.sentences 
        and return possible Rhyme for each letter in the rhyme pattern.

        Return:
          filtered_rhymes: Dict of pattern letters that maps to List of Rhyme objects.
            EX: {"A": [Rhyme1, Rhyme2]}

        """
        rhyme_counter = self.rhyme_by_metric()
        filtered_rhymes = {}
        for letter in rhyme_counter:
            sentences = self.sentences.copy()
            filtered_rhymes[letter] = self.metric_filter(
                sentences, rhyme_counter[letter])
        return filtered_rhymes

    def metric_filter(self, sentences, metrics):
        """ Return list of Rhyme objects that has the metrics.

        Parameters:
          metrics: List of metrics for each verse. EX: [10,10,9,9].

        """
        metric_counter = Counter(metrics)
        aux_sentences = []
        for rhyme in sentences:
            if rhyme.size(metric_counter):
                aux_sentences.append(rhyme)
        return aux_sentences

    def rhyme_by_metric(self):
        """ Represent rhyme pattern and metrics in one data structure.

        Example:
          Input: 
            self.rhyme: "AABB AACC"
            self.metric: [10, 10, 10, 10, 9, 9, 10, 10]
          Output: 
            letters: {"A":[10,10,9,9], "B":[10,10], "C":[10,10]}
        """
        letters = {}
        for i, r in enumerate(self.rhyme):
            if r not in letters:
                letters[r] = []
            letters[r].append(self.metric[i])
        return letters
