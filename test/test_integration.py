"""Minimum regression test

This test was made to avoid regressions while adding new tests
and refactoring the code.

This is not perfect, but ensures that the final behavior is the same,
considering the cuurent code is already working fine.
"""

import pytest


def run():
    from src.model.mives import Mives
    from src.model.poem_builder import PoemBuilder
    from src.model.filter import Filter
    import random

    padrao_ritmico: str = "ABAB ABAB CDC CDC"
    mives_xml: str = "xml/sentencas.xml"
    metrificacao: list[int] = [
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
    ]
    pesos_avaliacao: dict[str, int] = {
        "Rima toante & consoante": 1,
        "Acentuacao": 1,
        "Posicao tonica": 1,
        "Rima interna": 1,
        "Estrutura ritmica": 1,
    }
    seed: int = 1
    filename: str = "poem_test.txt"

    mives = Mives(mives_xml)
    metrics: list[int] = []

    for metric in metrificacao:
        if metric == "":
            metrics.append(random.randrange(6, 13))
        else:
            metrics.append(metric)

    print("Metricas:", metrics)
    sentences = Filter(
        mives.sentences, metrics, padrao_ritmico, seed
    ).get_rhymes()
    builder = PoemBuilder(
        sentences, metrics, padrao_ritmico, pesos_avaliacao, filename, seed
    )
    builder.build()
    builder.result()


def test_print_message(capfd) -> None:

    expected = """\
Metricas: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
A nação inteira interveio
Desafio o mundo inteiro
Afinal a multidão nterveio
Fora uma tenda de ferreiro

Ao contrário, este fortaleceu-o
Quebrou-se o encanto do conselheiro
Fazia calar o bombardeio
Acaba-se o desfiladeiro

Voltavam abatidos e exaustos
Moreira césar fora de combate
É a escarpa abrupta e viva dos planaltos

Lavraram incêndios em vários pontos
Quedavam numa mornidão irritante
Os comboios eram raros e incertos

Resultado:
 - Estrutura Ritmica: 0.535
 - Silabas Tônicas: 0.058
 - Acento: 1.0
 - Rima Interna: 0.045
 - Rima Toante & Consoante: 0.688
 Score Resultante: 0.419
"""

    run()
    actual, err = capfd.readouterr()

    assert expected == actual
    assert "" == err
