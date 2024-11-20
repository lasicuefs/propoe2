from typing import Any, Callable
import pytest

from src.api import Prosody, Weights


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
            rhythmic_structure=5,
        ).as_dict

        assert 1 == actual["Rima toante & consoante"]
        assert 2 == actual["Acentuacao"]
        assert 3 == actual["Posicao tonica"]
        assert 4 == actual["Rima interna"]
        assert 5 == actual["Estrutura ritmica"]


class DescribeProsody:
    @staticmethod
    def it_should_raise_for_larger_metrics():
        with pytest.raises(AssertionError):
            Prosody("AB BA", [10] * 5)

    @staticmethod
    def and_should_also_raise_for_smaller_metrics():
        with pytest.raises(AssertionError):
            Prosody("AB BA", [10] * 3)

    @staticmethod
    def but_should_not_raise_for_same_size():
        Prosody("AB BA", [10] * 4)

    @staticmethod
    @test(
        "Should ignore whitespaces when analizying the lenght of rhythm and rhymes"
    )
    def and_should_ignore_whitespace_for_rhymes():
        """
        This does not assert anything, because this is testing the AssertionError raising.
        Notice that both "AB BA" and "ABBA" are considered as being 4-lenght long rhymes.
        """
        assert Prosody("AB BA", [10] * 4) is not None
        assert Prosody("ABBA", [10] * 4) is not None

    @staticmethod
    def its_attributes_are_available():
        rhythm = [10] * 4
        rhyme = "AB BA"
        actual = Prosody("AB BA", [10] * 4)

        assert rhythm == actual.rhythm
        assert rhyme == actual.rhyme
        assert actual.rhyme == actual.pattern
