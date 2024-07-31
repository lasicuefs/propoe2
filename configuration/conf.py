#padrao_ritmico = "ABAB ABAB CDC CDC"
padrao_ritmico = "AABB"


mives_xml = "xml/sentencas.xml"  # Caminho para o XML do MIVES

# POEMA 3
# metrificacao = [10, 9, 9, 10]  # Metrica por verso

#metrificacao = ["", "", "", ""]

# POEMA 1 e 2
#metrificacao = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
# metrificacao = [10, 10, 10, 10]
metrificacao = [10, 10, 10, 10]

pesos_avaliacao = {
    "Rima toante & consoante": 0,
    "Acentuacao": 1,
    "Posicao tonica": 1,
    "Rima interna": 0,
    "Estrutura ritmica": 1
}

seed = None
filename = "poem.txt"
