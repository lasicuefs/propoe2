class Rhyme:
    """

    Attributes
    ----------
    rhyme: str
        Target rhyme of the end of a sentence.
        E.g. "ro".
    metrics: dict
        Maps the metric of a sentence to a list of Sentence objects
    """

    def __init__(self, rhyme):
        self.rhyme = rhyme
        self.metrics = {}

    def __eq__(self, other):
        return self.rhyme.strip() == other.rhyme.strip()

    def __repr__(self):
        return self.rhyme + ":\n" + str(self.metrics) + "\n"

    def not_in(self, sentences):
        # TODO: Technically this may be resumed to ``return self not in sentences``
        #   But first, I need to know what exactly type ``sentences`` takes.
        for sentence in sentences:
            if self == sentence:
                return False
        return True

    def add(self, sentence):
        """ Populate self.metrics.
        It adds a Sentence object to its correct metric with only the verses that has this metric.

        Return:
          self.metrics: Dict the maps the metric of a sentence to a list of Sentence objects.
            EX: {10: [Sentence1], 9: [Sentence2]}
        """
        metrics = []
        for verse in sentence.verse_structures:
            metric = int(verse.metric)
            if metric not in metrics:
                metrics.append(metric)
                if metric not in self.metrics:
                    self.metrics[metric] = []
                # Get Sentence object with only the verses with metric metric.
                m_sentence = sentence.get_metric(metric)
                self.metrics[metric].append(m_sentence)

    def remove_duplicates(self, sentences):
        """ Return a list of Sentence object that only appears once in the
        list sentences from parameters.

        Ex:
          Input: sentences = [Sentence1, Sentence1, Sentence2]
          Output: uniq_sentences = [Sentence2]
        """
        uniq_sentences = []
        iteration = len(sentences)
        for _ in range(iteration):
            sentence = sentences.pop(0)
            if sentence.not_in(sentences):
                uniq_sentences.append(sentence)
            sentences.append(sentence)
        return uniq_sentences

    def unique(self, sentences):
        """ Return a list of Sentence object removing duplicates inside list from parameters.

        Ex:
          Input: sentences = [Sentence1, Sentence1, Sentence2]
          Output: uniq_sentences = [Sentence1, Sentence2]
        """
        uniq_sentences = []
        for sentence in sentences:
            if sentence.not_in(uniq_sentences):
                uniq_sentences.append(sentence)
        return uniq_sentences

    def size(self, counter):
        """ Return True if this object is able to generate a poem.

        Object is able to generate a poem if it has the values needed in the counter
        parameter for each metric.

        Two cases return True:
        1. Object has more Sentence objects (removing repeted Sentence) than total amount
           of verses needed for rhyme pattern.
        2. Object has enough unique Sentece objects for each metric in the rhyme pattern.

        Parameters:
          counter: Dict mapping metric with its needed amount for the poem.
            EX: {10: 2, 9: 2}
        """

        if(self.check_sentences(counter)):
            return True
        else:
            metrics = self.get_unique_sentences(counter)
            if metrics:
                for m in counter:
                    if m in self.metrics:
                        result = 0
                        for metric in metrics:
                            if metric.verse_structures[0].metric == m:
                                result += 1
                        if result <= counter[m]:
                            return False
                    else:
                        return False
                return True
            else:
                return False

    def get_unique_sentences(self, counter):
        """ Merge List of Sentences with metrics in counter and return only the ones that
        appears once.

        Parameters:
          counter: Dict mapping metric with its needed amount for the poem.
            EX: {10: 2, 9: 2}
        """
        metrics = []
        for m in counter:
            if m in self.metrics:
                metrics.extend(self.metrics[m])
        # Get Sentence objects that only appears once
        metrics = self.remove_duplicates(metrics)
        return metrics

    def check_sentences(self, counter):
        """  Check if object has more Sentences objects (removing repeted Sentence) from each metric
        nedded for a verse than letters from rhyme patter. 

        Parameters:
          counter: Dict mapping metric with its needed amount for the poem.
            EX: {10: 2, 9: 2}
        """
        max_value = sum(counter.values())

        for m in counter:
            # If this Rhyme does not have a Sentence with this metric, return False
            if m in self.metrics:
                if len(self.unique(self.metrics[m])) > max_value:
                    return True
            else:
                return False
        return False
