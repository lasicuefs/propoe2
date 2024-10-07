padrao_ritmico = "ABAB ABAB CDC CDC"

mives_xml = "xml/sentencas.xml"  # Caminho para o XML do MIVES

# POEMA 3
# metrificacao = [10, 9, 9, 10]  # Metrica por verso

# metrificacao = ["", "", "", ""]

# POEMA 1 e 2
metrificacao = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

# POEMA 2
# pesos_avaliacao = {
#     "Rima toante & consoante": 0,
#     "Acentuacao": 1,
#     "Posicao tonica": 1,
#     "Rima interna": 2,
#     "Estrutura ritmica": 0
# }

# POEMA 1 e 3
pesos_avaliacao = {
    "Rima toante & consoante": 1,
    "Acentuacao": 1,
    "Posicao tonica": 1,
    "Rima interna": 1,
    "Estrutura ritmica": 1,
}

seed = None
filename = "poem.txt"
