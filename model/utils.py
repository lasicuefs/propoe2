import re
import string


def sentence_preprocess(sentence):
    """ Lower case sentence string and remove all pontuation and numbers
    """
    sentence = sentence.lower()
    sentence = re.sub(
        r'[^\w\sZáàâãéèêíïóôõöúçñ]', '', sentence)
    return sentence.strip()


def remove_space(sentence):
    return sentence.replace(" ", "")


def left_consonant_removal(sentence):
    """ Lower case sentence string and remove everything that is not vowel from the left
            side of the sentence.
    """
    sentence = sentence.lower()
    sentence = re.sub(
        r'[^aeiouáàâãéèêíïóôõöú]', '', sentence)
    return sentence.strip()


def consonant_removal(sentence):
    """ Lower case sentence string and remove everything that is not vowel.
    """
    sentence = sentence.lower()
    sentence = re.match(
        r'[aeiouáàâãéèêíïóôõöú][a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*$', sentence)
    return sentence.strip()


def remove_pontuation(word):
    """ Remove pontuation from a word
    """
    exclude = set(string.punctuation)
    last_syllable = ''.join(
        ch for ch in word if ch not in exclude)
    return last_syllable.strip()


def scanned_sentence_preprocess(sentence):
    """ Lower case sentence string and remove all pontuation and numbers, except "/".
    """
    sentence = sentence.lower()
    # Remove all pontuation
    sentence = re.sub(
        r'[^\w\sZáàâãéèêíïóôõöúçñ/]', '', sentence)
    return sentence.strip()


def remove_end_ponctuation(sentence):
    """ Remove pontuation at the end of a sentence
    """
    return re.sub("""^[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*
    |[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*$""", '', sentence)
