from model.mives import Mives
from model.poem_builder import PoemBuilder
from model.filter import Filter
from configuration.conf import *
import random

mives = Mives(mives_xml)
metrics = []
for metric in metrificacao:
    if metric == "":
        metrics.append(random.randrange(6, 13))
    else:
        metrics.append(metric)

print("Metricas:", metrics)

sentences = Filter(mives.sentences, metrics, padrao_ritmico, seed).get_rhymes()

builder = PoemBuilder(
    sentences, metrics, padrao_ritmico, pesos_avaliacao, filename, seed
)
builder.build()
builder.result()
