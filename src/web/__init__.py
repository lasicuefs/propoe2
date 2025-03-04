"""Endpoints of Propoe2's server

See http://127.0.0.1:8000/docs#/ for more information.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel

from src import api as propoe
from src.web.schemas.feedback import Feedback
from src.web.schemas.prosody import Prosody
from src.web.schemas.weights import Weights
from src.web.schemas.poem import Poem

logger.add(
    "logs/request.log",
    format="{time:YYYY-MM-DD} | Action: Request at /{extra[route]}/ | {message}",
    encoding="UTF-8",
    filter=lambda record: "request" in record["extra"],
)

logger.add(
    "logs/feedback.log",
    format="{time:YYYY-MM-DD} | Action: Feedback | ⭐ {extra[stars]} : {message}",
    encoding="UTF-8",
    filter=lambda record: "feedback" in record["extra"],
)

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

    result = propoe.Propoe(
        filename="poem_test_api.txt",
        mives_file="xml/sentencas.xml",
        prosody=entry.prosody.as_domain(),
        evaluation_weights=entry.weights.as_domain(),
    ).poem

    logger.bind(request=True).info(
        f"Poem '{entry.prosody.pattern}' requested!", route="poem"
    )
    return Poem.from_domain(result)


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

    logger.bind(request=True).info("Sample requested!", route="sample")
    return Poem.from_domain(result)


@app.post("/feedback/")
async def feedback(feed: Feedback) -> None:
    """Logs User's feedback about Propoe"""

    logger.bind(request=True).info("Feedback submited!", route="feedback")

    inlined_comment = feed.comment.replace("\n", "¶ ")
    logger.bind(feedback=True).info(inlined_comment, stars=feed.stars)
