from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src import api as propoe
from src.web.schemas.prosody import Prosody
from src.web.schemas.weights import Weights
from src.web.schemas.poem import Poem

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://localhost:4200",
        "http://127.0.0.1:4200",
        "https://127.0.0.1:4200",
        "http://rickbarretto.github.io/propoe2-ui/",
        "https://rickbarretto.github.io/propoe2-ui/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entry(BaseModel):
    prosody: Prosody
    weights: Weights

@app.post("/poem/")
async def poem(entry: Entry) -> Poem:
    result = propoe.Propoe(
        filename="poem_test_api.txt",
        mives_file="xml/sentencas.xml",
        prosody=entry.prosody.as_domain(),
        evaluation_weights=entry.weights.as_domain(),
    ).poem

    return Poem.from_domain(result)

@app.get("/sample/")
async def sample() -> Poem:
    prosody = propoe.Prosody(
        "ABAB ABAB CDC CDC",
        [10] * 14,
    )

    weights = propoe.Weights()

    result = propoe.Propoe(
        filename="poem_test_api.txt",
        mives_file="xml/sentencas.xml",
        prosody=prosody,
        evaluation_weights=weights,
    ).poem

    return Poem.from_domain(result)
