from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

#load
nltk.download('punkt_tab')
nltk.download('stopwords')


class Preprocessing:
    def preprocessing(self, text):
        return word_tokenize(text.lower())

    #return self.removeStopwords(word_tokenize(text.lower()))

    def removeStopwords (self, sentenceList:list):
        pt_stopwords = stopwords.words('portuguese')
        filterList = [word for word in sentenceList if word not in pt_stopwords]
        return filterList