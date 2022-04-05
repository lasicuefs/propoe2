import re


class Sentence ():

    def __init__(self, sentence, link, sentence_number, verse_structures):
        self.sentence = self.remove_end_ponctuation(sentence)
        self.link = link
        self.sentence_number = sentence_number
        self.verse_structures = verse_structures

    def remove_end_ponctuation(self, sentence):
        return re.sub('^[^a-zA-Z]*|[^a-zA-Z]*$', '', sentence)

    def __eq__(self, other):
        return self.sentence == other.sentence

    def __hash__(self):
        return hash(('sentence', self.sentence))

    def __repr__(self):
        verses_repr = "\n".join([verse.__repr__()
                                for verse in self.verse_structures])
        return ("\n\n Sentence: " + self.sentence +
                "\n link: " + str(self.link) +
                "\n sentence number: " + str(self.sentence_number) +
                "\n Verses: " + verses_repr)

    def not_in(self, sentences):
        sentence = self.sentence.lower()
        sentence = re.sub(r'[^\w\s]', '', sentence)

        for b_sentence in sentences:
            b_sentence = b_sentence.sentence.lower()
            b_sentence = re.sub(r'[^\w\s]', '', b_sentence)
            if b_sentence == sentence:
                return False
        return True
