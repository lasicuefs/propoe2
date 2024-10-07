from collections import Counter
import random

from model.rhyme import Rhyme
from .utils import remove_space


class Filter:
    """

    Attributes
    ----------
    setences: list[Rhyme]
        List of Rhyme objects
    metric: list
        List of metrics for each verse
    rhyme: str
        Rhyme Pattern
        E.g. "AABB CCDD"
    choosen_rhymes: list[Rhyme]
        List of Rhyme objects
    """

    def __init__(
        self, sentences: list[Rhyme], metric, rhyme_pattern: str, seed
    ) -> None:
        # TODO: is ``sentences`` a ``list[Rhyme]`` or ``list[Sentence]``?
        # TODO: define what ``metric`` is
        # TODO: define what ``seed`` is
        self.sentences: list[Rhyme] = sentences
        self.metric = metric
        self.rhyme: str = remove_space(rhyme_pattern)
        self.chosen_rhymes: list[Rhyme] = []
        random.seed(seed)

    def get_rhymes(self) -> dict[str, Rhyme]:
        """Return which Rhyme objects to use for each letter in the rhyme pattern.

        Return:
          sentences: Dict of letters from rhyme pattern that maps to a Rhyme object
            EX: {"A": Rhyme, "B": Rhyme}

        """
        rhymes = self.rhyme_filter()
        sentences = {}
        # TODO: is it iterating keys or values?
        #   Consider using .keys() or .items()
        for letter in rhymes:
            sentences[letter] = self.random_rhyme(rhymes[letter])
        return sentences

    def random_rhyme(self, rhymes):
        """Return a random Rhyme object inside a list of Rhyme objects"""
        number = random.randrange(len(rhymes))
        rhyme = rhymes[number]
        if rhyme.not_in(self.chosen_rhymes):
            self.chosen_rhymes.append(rhyme)
            return rhyme
        else:
            return self.random_rhyme(rhymes)

    def rhyme_filter(self) -> dict[str, list[Rhyme]]:
        """Filter Rhyme object inside self.sentences
        and return possible Rhyme for each letter in the rhyme pattern.

        Return:
          filtered_rhymes: Dict of pattern letters that maps to List of Rhyme objects.
            EX: {"A": [Rhyme1, Rhyme2]}

        """
        rhyme_counter = self.rhyme_by_metric()
        filtered_rhymes = {}
        # TODO: is it iterating keys or values?
        #   Consider using .keys() or .items()
        for letter in rhyme_counter:
            sentences = self.sentences.copy()
            filtered_rhymes[letter] = self.metric_filter(
                sentences, rhyme_counter[letter]
            )
        return filtered_rhymes

    def metric_filter(self, sentences, metrics) -> list[int]:
        """Return list of Rhyme objects that has the metrics.

        Parameters:
          metrics: List of metrics for each verse. EX: [10,10,9,9].

        """
        metric_counter = Counter(metrics)
        aux_sentences = []
        for rhyme in sentences:
            if rhyme.size(metric_counter):
                aux_sentences.append(rhyme)
        return aux_sentences

    def rhyme_by_metric(self) -> dict[str, list[int]]:
        """Represent rhyme pattern and metrics in one data structure.

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
