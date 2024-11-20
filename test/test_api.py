from src.api import Propoe, Prosody, Weights

def test_determinism():
    """Propoe should not return different poems for the same instance.

    This should also be valid when the seed is not set.
    """

    propoe = Propoe(
        filename="poem_test.txt",
        mives_file="xml/sentences.xml",
        evaluation_weights=Weights(),
        prosody=Prosody(
            "AB AB", [10, 7, 7, 10]
        ),
        seed=None
    )

    propoe.poem == propoe.poem
    propoe.evaluation == propoe.evaluation