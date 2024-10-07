# TODO: ``remove_end_ponctuation`` is missing
from model.verse_structure import Verse_structure
from .utils import remove_end_ponctuation, sentence_preprocess


class Sentence:

    def __init__(self, sentence, link, sentence_number, verse_structures: list[Verse_structure]) -> None:
        # TODO: Is ``sentence`` a Sentence?
        # TODO: What is ``link``?
        # TODO: What is ``sentence_number``?

        self.sentence = sentence
        self.link = link
        self.sentence_number = sentence_number
        self.verse_structures: list[Verse_structure] = verse_structures

    def __eq__(self, other) -> bool:
        sentence = sentence_preprocess(self.sentence)
        other = sentence_preprocess(other.sentence)
        return sentence.split()[-1].strip() == other.split()[-1].strip()

    def __hash__(self) -> int:
        return hash(('sentence', self.sentence))

    def __repr__(self) -> str:
        verses_repr = "\n".join([verse.__repr__()
                                for verse in self.verse_structures])
        return ("\n\n Sentence: " + self.sentence +
                "\n link: " + str(self.link) +
                "\n sentence number: " + str(self.sentence_number) +
                "\n Verses: " + verses_repr)

    def not_in(self, sentences: list["Sentence"]) -> bool:
        # TODO: Technically this may be resumed to ``return self not in sentences``
        #   But first, I need to know what exactly type ``sentences`` takes.
        #   If sentences is a type that has the __contains__ method,
        #   this method is completely redundant, and should be deprecated.
        for sentence in sentences:
            if self == sentence:
                return False
        return True

    def get_metric(self, metric) -> "Sentence":
        # What is ``metric``?
        """ Return a Sentence object with Verse_structures that has metric egual m.
        """
        verses = [verse for verse in self.verse_structures if verse.metric == metric]
        return Sentence(self.sentence, self.link, self.sentence_number, verses)
