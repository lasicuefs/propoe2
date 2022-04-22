padrao_ritmico = "AABB AACC"

mives_xml = "xml/sentencas.xml"  # Caminho para o XML do MIVES

caminho_poema = "poemas/poema.txt"  # Se None, não salva poema

metrificacao = [10, 10, 10, 10, 9, 9, 10, 10]  # Metrica por verso

# Peso entre 0 e 1.
pesos_avaliacao = {
    "Rima consoante": 1,
    "Acentuacao": 1,
    "Posicao tonica": 1,
    # "Rima toante": 1,
    "Rima interna": 1,
    "Estrutura ritmica": 1
}
