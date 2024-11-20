from typing import Any, Callable
import pytest

from src.api import Weights


def test(desc: str) -> Callable[..., Any]:
    def wrapper(func: Callable[..., Any]):
        return func
    return wrapper   


class DescribeWeights:

    @staticmethod
    def it_should_init_everything_as_one():
        actual = Weights()

        assert 1 == actual.vocal_harmony
        assert 1 == actual.accentuation
        assert 1 == actual.tonic_position
        assert 1 == actual.internal_rhyme
        assert 1 == actual.rhythmic_structure

    @staticmethod
    def and_should_maps_internal_dict_api():
        actual = Weights(
            vocal_harmony=1,
            accentuation=2,
            tonic_position=3,
            internal_rhyme=4,
            rhythmic_structure=5
        ).as_dict

        assert 1 == actual["Rima toante & consoante"]
        assert 2 == actual["Acentuacao"]
        assert 3 == actual["Posicao tonica"]
        assert 4 == actual["Rima interna"]
        assert 5 == actual["Estrutura ritmica"]

