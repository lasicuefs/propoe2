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
        for sentence in sentences:
            if sentence.not_in(uniq_sentences):
                uniq_sentences.append(sentence)
        return uniq_sentences

    def size(self, m):
        if m in self.metrics:
            return len(self.remove_duplicates(self.metrics[m]))
        return 0
