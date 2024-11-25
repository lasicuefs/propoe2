from fastapi import FastAPI

from src.api import Poem, Propoe, Prosody, Weights

app = FastAPI()

@app.get("/poem/")
async def poem(prosody: Prosody, weights: Weights = Weights()):
    poem = Propoe(
        filename="poem_test_api.txt",
        mives_file="xml/sentencas.xml",
        prosody=prosody,
        evaluation_weights=weights
    ).poem

    return {
        "status": "OK",
        "content": poem.content,
        "evaluation": poem.evaluation,
    }


@app.get("/sample/")
async def sample():
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

    return {
        "content": poem.content,
        "evaluation": poem.evaluation,
    }