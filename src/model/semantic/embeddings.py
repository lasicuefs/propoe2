from transformers import AutoTokenizer,AutoModel
from sentence_transformers import SentenceTransformer

#Load Models
tokenizer_bertimbal = AutoTokenizer.from_pretrained("neuralmind/bert-large-portuguese-cased")
model_bertimbal = AutoModel.from_pretrained('neuralmind/bert-large-portuguese-cased')
word2vec_skip_s1000 = SentenceTransformer("mteb-pt/average_pt_nilc_word2vec_skip_s1000")

