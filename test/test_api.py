from pytest import skip
from src.api import Propoe, Prosody, Weights


@skip("This cannot be ensured since this depends on the internal API, which disallows this.")
def test_determinism():
    """Propoe should not return different poems for the same instance.

    This should also be valid when the seed is not set.
    """

    propoe = Propoe(
        filename="poem_test.txt",
        mives_file="xml/sentencas.xml",
        evaluation_weights=Weights(),
        prosody=Prosody("AB AB", [10, 7, 7, 10]),
        seed=None,
    )

    assert propoe.poem.content == propoe.poem.content
    assert propoe.poem.evaluation == propoe.poem.evaluation
