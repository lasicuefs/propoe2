from fastapi import FastAPI

from src import api as propoe
from src.web import schemas

app = FastAPI()


@app.get("/poem/")
async def poem(
    prosody: propoe.Prosody, weights: propoe.Weights = propoe.Weights()
) -> schemas.Poem:
    poem = propoe.Propoe(
        filename="poem_test_api.txt",
        mives_file="xml/sentencas.xml",
        prosody=prosody,
        evaluation_weights=weights,
    ).poem

    return schemas.Poem.from_poem(poem)


@app.get("/sample/")
async def sample() -> schemas.Poem:
    prosody = propoe.Prosody(
        "ABAB ABAB CDC CDC",
        [10] * 14,
    )

    weights = propoe.Weights()

    poem = propoe.Propoe(
        filename="poem_test_api.txt",
        mives_file="xml/sentencas.xml",
        prosody=prosody,
        evaluation_weights=weights,
    ).poem

    return schemas.Poem.from_poem(poem)
