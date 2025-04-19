from dataclasses import dataclass
import random

from src.model.poem import Poem
from src.model.rhyme import Rhyme
from src.model.score import *
from src.model.poem_evaluation import Evaluation
from src.model.utils import remove_end_ponctuation
import sys


@dataclass
class PoemBuilder:
    """

    Attributes
    ----------
    sentences: dict[str, Rhyme]
        List of Rhyme objects
    rhyme: str
        Rhyme Pattern. E.g.: "AABB CCDD"
    metrics: list[int]
        List of metrics per verse
    poem: str
        maps score name and its weight
    score_weight: dict[str, float]
        Score Weight for the poem evaluation
    evaluation: Evaluation
        The evaluation of the Poem
    orig_stdout: TextIO
        The original System's Stdout
    f: TextIOWrapper[_WrappedBuffer]
        The file reference for the filename with "write" access.
    """

    sentences: dict[str, Rhyme]
    metrics: list[int]
    rhyme: str
    score_weight: dict[str, float]
    _filename: str
    _seed: int | None


    def __post_init__(self):
        self.metric_count = 0
        self.last_rhyme = {}
        self.poem_sentences = {}
        self.poem_scores = {}
        self.poem: Poem
        random.seed(self._seed)

        self.orig_stdout = sys.stdout
        self.f = open(self._filename, "w", encoding="UTF-8")
        sys.stdout = self.f

    def result(self) -> None:
        print(self.poem)
        print(self.poem.poem_score)

    def save(self, path) -> None:
        """Save poem in txt file."""
        text_file = open(path, "w", encoding="UTF-8")
        text_file.write(self.poem)
        text_file.close()

    def build(self) -> None:
        """Build poem. Get best sentences and add it in the string self.poem."""
        sentences = self.get_poem_sentences()
        self.poem = self.buil_poem_result(sentences)
        sys.stdout = self.orig_stdout
        self.f.close()

    def buil_poem_result(self, sentences):
        verses = []
        verses_score = []
        verses_score_list = []
        scanned_verses = []

        for letter in self.rhyme:
            if letter != " ":
                s = sentences[letter].pop(0)
                verses.append(remove_end_ponctuation(s.sentence).capitalize())
                scanned_verses.append(s.verse_structures[0].scanned_sentence)
                poem_score = self.poem_scores[letter].pop(0)
                verses_score_list.append(poem_score)
                if poem_score:
                    verses_score.append(poem_score.score)
                else:
                    verses_score.append(Score())

        return Poem(verses=verses, verses_score=verses_score, scanned_verses=scanned_verses, poem_score=PoemScore(verses_score_list).score, poem_structure=self.rhyme)

    def random_sentence(self, letter):
        sentence_metric_list = self.sentences[letter].metrics[
            self.metrics[self.metric_count]
        ]
        sentence_index = random.randrange(len(sentence_metric_list))
        sentence = sentence_metric_list[sentence_index]
        if sentence.not_in(self.poem_sentences[letter]):
            return sentence
        else:
            return self.random_sentence(letter)

    def random_verse_structures(self, sentence):
        number = random.randrange(len(sentence.verse_structures))
        return sentence.verse_structures[number]

    def initialize_sentences(self):
        """Initializa a Dict mapping the letters from the rhyme pattern to an empty list."""
        self.poem_sentences = {}
        self.poem_scores ={}
        for letter in self.sentences:
            self.poem_sentences[letter] = []
            self.poem_scores[letter] = []

    def get_poem_sentences(self):
        """Return a list of Sentence objects in order to build a poem."""
        self.initialize_sentences()
        self.last_rhyme = {}         # Dict that maps letters from rhyme pattern to its last Rhyme object
        self.metric_count = 0         # Index from self.metrics that shows with metric does this Sentence object needs.
        new_strophe = True
        current_verse_structures = None
        ref_verse_structures = None

        # Iterate through every letter from rhyme pattern, one by one, in order.
        for letter in self.rhyme:
            if letter == " ":
                new_strophe = True
            elif new_strophe:
                current_verse_structures = self.start_new_strophe(letter)
                ref_verse_structures = current_verse_structures
                new_strophe = False
            else:
                current_verse_structures = self.new_verse_by_score(current_verse_structures, letter, ref_verse_structures)

        return self.poem_sentences

    def reference_verse_rhyme(self, letter):
        # If not a new rhyme, if there is a verse we can compare to.
        if letter in self.last_rhyme:
            # Last Verse object that rhymes with the new verse to be found.
            return self.last_rhyme[letter]
        return None

    def new_verse_by_score(self, current_verse_structures, letter, ref_verse_structures):
        verse_rhyme = self.reference_verse_rhyme(letter)
        current_verse, current_verse_structures, verse_score = self.find_sentence(
            [current_verse_structures, ref_verse_structures],
            letter,
            verse_rhyme)
        self.add_new_verse(letter,current_verse_structures, current_verse, verse_score)
        return current_verse_structures

    def start_new_strophe(self, letter):
        current_verse = self.random_sentence(letter)
        current_verse_structures = self.random_verse_structures(current_verse)
        self.add_new_verse(letter, current_verse_structures, current_verse, None)
        print(current_verse_structures.scanned_sentence + "\n")
        return current_verse_structures

    def add_new_verse(self, letter, current_verse_structures, current_verse, verse_score):
        self.last_rhyme[letter] = current_verse_structures
        self.poem_sentences[letter].append(current_verse)
        self.poem_scores[letter].append(verse_score)
        self.metric_count += 1

    # TODO: define missing types
    def find_sentence(
        self,
        verses: list,
        letter: str,
        last_rhyme,
    ):
        """Return best Sentence object given a score.

        Parameters:
          sentences: List of Sentence objects chosen for the current poem.
          verses: List with only the first Verse object of strophe and the current Verse object.
          letter: Which rhyme pattern it is. EX: "A", "B" or "C".
          last_rhyme: Verse object of the last Sentence that rhymes.
          metric_count: Index from self.metrics that shows with metric does
            this Sentence object needs.

        Return:
          next_s: Chosen Sentence object
          next_verse: Chosen Verse object from the Sentence object
        """
        max_score = -1
        count = 0
        candidate_sentences = self.sentences[letter].metrics[
            self.metrics[self.metric_count]]
        for sentence in candidate_sentences:
            if sentence.not_in(self.poem_sentences[letter]):
                verse_structures = sentence.verse_structures[0]
                verse_score = VerseScore(verse_structures.scanned_sentence)
                count += 1
                print("------------------")
                for verse in verses:
                    verse_score.score_calculation(verse, verse_structures, last_rhyme, self.score_weight)

                    print(verse_score)
                    print()
                    if verse_score.score.score_result > max_score:
                        max_score = verse_score.score.score_result
                        next_verse = sentence
                        next_verse_structure = verse_structures
                        result_score = verse_score
        print("------------ESCOLHIDO----------------")
        print("Quantidade de versos:", str(count))
        # TODO: ``result_score`` may never be assigned
        print(result_score)
        print()

        # self.evaluation.add(result_score)
        # TODO: ``next_s`` and ``next_verse`` may never be assigned
        return next_verse, next_verse_structure, result_score
