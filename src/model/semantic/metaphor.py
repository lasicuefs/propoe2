import torch
from transformers import pipeline, AutoTokenizer,AutoModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.model.semantic.semanticSimilarity import SemanticSimilarity
import re


model_bertimbal = AutoModel.from_pretrained('neuralmind/bert-large-portuguese-cased')
tokenizer_bertimbal = AutoTokenizer.from_pretrained('neuralmind/bert-large-portuguese-cased')
pipe = pipeline('fill-mask', model="neuralmind/bert-large-portuguese-cased", tokenizer=tokenizer_bertimbal)


class Metaphor:

    def __init__(self):
        self.__pt_stopwords = stopwords.words('portuguese')
        self.semantic_similarity = SemanticSimilarity()

    def removeStopwords(self, sentenceList: list):
        filterList = [word for word in sentenceList if word.lower() not in self.__pt_stopwords]
        return filterList

    def convertSetenceInEmbeddingVectorTorch(self, sentence, model, tokenizer):
        input_ids = tokenizer.encode(sentence, return_tensors='pt')
        with torch.no_grad():
            outs = model(input_ids)
            encoded = outs[0][0, 1:-1]
            return encoded.tolist()

    def metaphor_degree(self, sentenca):
      tokenize_sentence = word_tokenize(re.sub(r'[^\w\s-]', '', sentenca))
      filtered = self.removeStopwords(tokenize_sentence)
      embedding = self.convertSetenceInEmbeddingVectorTorch(" ".join(filtered), model_bertimbal, tokenizer_bertimbal)
      similarity_max = 0

      for index in range(0, len(filtered)):
        embedding_copy = embedding.copy()
        embedding_copy.pop(index)
        if len(embedding_copy) > 0:
          word_target = filtered[index]
          if word_target in sentenca:
              sentence_mask = sentenca.replace(word_target, "[MASK]")
              possible_words_set = pipe(sentence_mask)
              fit_word = possible_words_set[0]['token_str']
              similarity = self.semantic_similarity.similaritry_between_words_bert(fit_word, word_target,model_bertimbal, tokenizer_bertimbal)
              if similarity > similarity_max:
                similarity_max = similarity
          else:
              raise RuntimeError(f" Targert word {word_target} não existe na sentença {sentenca}, the list of filter word is {filtered}")
      return  1 - similarity_max