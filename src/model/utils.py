import re
import string


def sentence_preprocess(sentence: str) -> str:
    """Lower case sentence string and remove all pontuation and numbers"""
    sentence = sentence.lower()
    sentence = re.sub(r"[^\w\sZáàâãéèêíïóôõöúçñ]", "", sentence)
    return sentence.strip()


def remove_space(sentence: str) -> str:
    # TODO: This returns a ``str``, I guess
    return sentence.replace(" ", "")


def left_consonant_removal(sentence: str) -> str:
    """Lower case sentence string and remove everything that is not vowel from the left
    side of the sentence.
    """
    sentence = sentence.lower()
    sentence = re.sub(r"[^aeiouáàâãéèêíïóôõöú]", "", sentence)
    return sentence.strip()


def consonant_removal(sentence) -> str:
    # TODO: What is ``sentence`` in this case?
    # TODO: I guess the return type should be a ``str``
    """Lower case sentence string and remove everything that is not vowel."""
    sentence = sentence.lower()
    sentence = re.match(
        r"[aeiouáàâãéèêíïóôõöú][a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*$", sentence
    )
    # TODO: re.match returns ``Match[str]`` or ``None``
    #   So, technically, we can't use ``str.strip``.
    return sentence.strip()


def remove_pontuation(word: str) -> str:
    """Remove pontuation from a word"""
    exclude = set(string.punctuation)
    last_syllable = "".join(ch for ch in word if ch not in exclude)
    return last_syllable.strip()


def scanned_sentence_preprocess(sentence: str) -> str:
    """Lower case sentence string and remove all pontuation and numbers, except "/"."""
    sentence = sentence.lower()
    # Remove all pontuation
    sentence = re.sub(r"[^\w\sZáàâãéèêíïóôõöúçñ/]", "", sentence)
    return sentence.strip()


def remove_end_ponctuation(sentence: str) -> str:
    """Remove pontuation at the end of a sentence"""
    return re.sub(
        """^[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*
    |[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*$""",
        "",
        sentence,
    )
