"""Endpoints of Propoe2's server

See http://127.0.0.1:8000/docs#/ for more information.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src import api as propoe
from src.web.logging import PropoesEvent
from src.web.schemas.feedback import Feedback
from src.web.schemas.prosody import Prosody
from src.web.schemas.weights import Weights
from src.web.schemas.poem import Poem

propoe_event = PropoesEvent()

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
    """Entry Scheme for the /poem/ endpoint"""

    prosody: Prosody
    weights: Weights


@app.post("/poem/")
async def poem(entry: Entry) -> Poem:
    """Generate a Poem from an Json entry."""

    result = Poem.from_domain(
        propoe.Propoe(
            filename="poem_test_api.txt",
            mives_file="xml/sentencas.xml",
            prosody=entry.prosody.as_domain(),
            evaluation_weights=entry.weights.as_domain(),
        ).poem
    )

    await propoe_event.route_requested(
        "poem", f"Poem '{entry.prosody.pattern}' requested!"
    )
    await propoe_event.poem_created(result)

    return result


@app.get("/sample/")
async def sample() -> Poem:
    """Generates a default random sample of the Poem.

    By default, this sample is in the format "ABAB ABAB CDC CDC",
    with 10 phonetic sylables each.
    """

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

    await propoe_event.route_requested("sample", "Sample requested!")
    return Poem.from_domain(result)


@app.post("/feedback/")
async def feedback(feed: Feedback) -> None:
    """Logs User's feedback about Propoe"""

    await propoe_event.route_requested("feedback", "Feedback submited!")
    await propoe_event.feedback_submited(feed.comment, feed.stars)
