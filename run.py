from model.mives import Mives
from model.poem_builder import Poem_builder
from model.filter import Filter
from model.evaluation import Evaluation

rhyme = 'AACC AADD'
mives = Mives('xml/sentencas.xml')
chosen_rhymes = Filter(mives.sentences).rhyme_filter(rhyme)
print('Rhymes:', chosen_rhymes)
print()
builder = Poem_builder(mives.sentences, chosen_rhymes, rhyme)
builder.build()
print(builder.poem)
# evaluation = Evaluation(builder.verse_list)
# print(evaluation.score)
