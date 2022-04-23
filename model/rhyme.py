class Rhyme():

    def __init__(self, rhyme):
        self.rhyme = rhyme
        self.metrics = {}

    def __repr__(self):
        return self.rhyme + ":\n" + str(self.metrics) + "\n"

    def add(self, sentence):
        metrics = []
        for verse in sentence.verse_structures:
            metric = int(verse.metric)
            if metric not in metrics:
                metrics.append(metric)
                if metric not in self.metrics:
                    self.metrics[metric] = []
                m_sentence = sentence.get_metric(metric)
                self.metrics[metric].append(m_sentence)

    def remove_duplicates(self, sentences):
        uniq_sentences = []
        iteration = len(sentences)
        for _ in range(iteration):
            sentence = sentences.pop()
            if sentence.not_in(sentences):
                uniq_sentences.append(sentence)
        return uniq_sentences

    def unique(self, sentences):
        uniq_sentences = []
        for sentence in sentences:
            if sentence.not_in(uniq_sentences):
                uniq_sentences.append(sentence)
        return uniq_sentences

    def size(self, counter):
        max_value = sum(counter.values())
        check = True
        counter2 = {}
        for m in counter:
            if m in self.metrics:
                if len(self.unique(self.metrics[m])) < max_value:
                    check = False
                    counter2[m] = max_value - len(self.unique(self.metrics[m]))
            else:
                return False

        if not check:
            metrics = []
            for m in counter2:
                metrics.extend(self.metrics[m])
            metrics = self.remove_duplicates(metrics)
            for m in counter2:
                result = 0
                for metric in metrics:
                    if metric.verse_structures[0].metric == m:
                        result += 1
                if result <= counter2[m]:
                    return False
            return True
        else:
            return True
