from src.model.semantic.preprocessing import Preprocessing
import math
import torch
class SemanticSimilarity:

    def __init__(self):
        self.preprocessing = Preprocessing()

    def similaritry_between_words_bert(self, s1, s2, model, tokenizer):
        s1_embedding = self.convertSetenceInEmbeddingVectorTorch(s1, model, tokenizer)
        s2_embedding = self.convertSetenceInEmbeddingVectorTorch(s2, model, tokenizer)
        return EmbeddingSimilarity.cossineSimilarity(s1_embedding[0], s2_embedding[0])

    def convertSetenceInEmbeddingVectorTorch(self, sentence, model, tokenizer):
        input_ids = tokenizer.encode(sentence, return_tensors='pt')
        with torch.no_grad():
            outs = model(input_ids)
            encoded = outs[0][0, 1:-1]
            return encoded.tolist()

    def preprocessingSentences(self, s1, s2, model):
        s1_embedding = model.encode([s1.lower()])
        s2_embedding = model.encode([s2.lower()])

        return s1_embedding, s2_embedding

    def cossineSimilarity(self, s1, s2, model):
        mean_s1, mean_s2 = self.preprocessingSentences(s1, s2, model)
        return EmbeddingSimilarity.cossineSimilarity(mean_s1[0], mean_s2[0])


class EmbeddingSimilarity:

    @staticmethod
    def cossineSimilarity(s1, s2):
        size = len(s1)
        sum = 0
        square_sum_s1 = 0
        square_sum_s2 = 0

        for index in range(size):
            sum += s1[index] * s2[index]
            square_sum_s1 += s1[index] ** 2
            square_sum_s2 += s2[index] ** 2

        if square_sum_s2 == 0 or square_sum_s1 == 0:
            return 0

        return sum / (math.sqrt(square_sum_s1) * math.sqrt(square_sum_s2))

