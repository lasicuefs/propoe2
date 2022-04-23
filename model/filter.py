from collections import Counter
import random


class Filter():
    def __init__(self, sentences, metric, seed):
        self.sentences = sentences
        self.metric = metric
        self.rhyme_numbers = []
        random.seed(seed)

    def get_rhymes(self, rhyme):
        rhymes = self.rhyme_filter(rhyme)
        sentences = {}
        for letter in rhymes:
            sentences[letter] = self.random_rhyme(rhymes[letter])
        return sentences

    def random_rhyme(self, rhymes):
        number = random.randrange(len(rhymes))
        if number not in self.rhyme_numbers:
            self.rhyme_numbers.append(number)
            return rhymes[number]
        else:
            return self.random_rhyme(rhymes)

    def rhyme_filter(self, rhyme):
        rhyme = self.remove_space(rhyme)
        rhyme_counter = self.rhyme_by_metric(rhyme)
        filtered_rhymes = {}
        for letter in rhyme_counter:
            sentences = self.sentences.copy()
            metric_counter = Counter(rhyme_counter[letter])
            aux_sentences = []
            for rhyme in sentences:
                if rhyme.size(metric_counter):
                    aux_sentences.append(rhyme)
            filtered_rhymes[letter] = aux_sentences
        return filtered_rhymes

    def rhyme_by_metric(self, rhyme):
        letters = {}
        for i, r in enumerate(rhyme):
            if r not in letters:
                letters[r] = []
            letters[r].append(self.metric[i])
        return letters

    def remove_space(self, rhyme):
        return rhyme.replace(" ", "")
