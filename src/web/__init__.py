from fastapi import FastAPI

from src.api import Propoe, Prosody, Weights
from src.web import schemas

app = FastAPI()


@app.get("/poem/")
async def poem(prosody: Prosody, weights: Weights = Weights()) -> schemas.Poem:
    poem = Propoe(
        filename="poem_test_api.txt",
        mives_file="xml/sentencas.xml",
        prosody=prosody,
        evaluation_weights=weights,
    ).poem

    return schemas.Poem.from_poem(poem)


@app.get("/sample/")
async def sample() -> schemas.Poem:
    prosody = Prosody(
        "ABAB ABAB CDC CDC",
        [10] * 14,
    )

    weights = Weights()

    poem = Propoe(
        filename="poem_test_api.txt",
        mives_file="xml/sentencas.xml",
        prosody=prosody,
        evaluation_weights=weights,
    ).poem

    return schemas.Poem.from_poem(poem)
