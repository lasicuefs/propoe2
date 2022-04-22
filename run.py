from model.mives import Mives
from model.poem_builder import Poem_builder
from model.filter import Filter
from configuration.conf import *

seed = None

mives = Mives(mives_xml)
chosen_rhymes = Filter(mives.sentences, seed).rhyme_filter(padrao_ritmico)
builder = Poem_builder(mives.sentences, chosen_rhymes,
                       padrao_ritmico, pesos_avaliacao, seed)
builder.build(verbose=True)
builder.result()
builder.save(caminho_poema)
