class Rhyme():

    def __init__(self, rhyme):
        # EX: "ro", end of a sentence.
        self.rhyme = rhyme
        # Dict the maps the metric of a sentence to a list of Sentence objects.
        self.metrics = {}

    def __eq__(self, other):
        return self.rhyme.strip() == other.rhyme.strip()

    def __repr__(self):
        return self.rhyme + ":\n" + str(self.metrics) + "\n"

    def not_in(self, sentences):
        for sentence in sentences:
            if self.__eq__(sentence):
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
        1. Object has more Sentence objects (removing repeted Sentence) from each metric
           needed for verse than letters needed from rhyme patter.
        2. Object has enouth unique Sentece objects for each metric in the rhyme pattern.

        Parameters:
          counter: Dict mapping metric with its needed amount for the poem.
            EX: {10: 2, 9: 2}
        """

        counter2 = self.check_sentences(counter)
        if counter2 == "no metric":
            return False

        # If there are Sentences needed for rhyme pattern and metric.
        if counter2:
            metrics = self.get_unique_sentences(counter2)
            # Check unique Sentence objects from metrics
            for m in counter2:
                result = 0
                for metric in metrics:
                    if metric.verse_structures[0].metric == m:
                        result += 1
                # If not enough Sentences to make the poem.
                if result <= counter2[m]:
                    return False
            return True
        else:
            return True

    def get_unique_sentences(self, counter):
        """ Merge List of Sentences with metrics in counter and return onlt the ones that
        appears once.

        Parameters:
          counter: Dict mapping metric with its needed amount for the poem.
            EX: {10: 2, 9: 2}
        """
        metrics = []
        for m in counter:
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

        Return:
          EITHER:
            "no metric": String to say that there is not metric.
          OR:
            counter2: Dict that maps metric to the needed amount of unique Sentence 
                      object for each metric for the verses in the rhyme pattern.
        """
        max_value = sum(counter.values())
        counter2 = {}

        for m in counter:
            # If this Rhyme does not have a Sentence with this metric, return False
            if m in self.metrics:
                if len(self.unique(self.metrics[m])) < max_value:
                    counter2[m] = max_value - len(self.unique(self.metrics[m]))
            else:
                return "no metric"
        return counter2
