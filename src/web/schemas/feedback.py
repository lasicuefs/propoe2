"""User's Feedback Schemas"""

from pydantic import BaseModel, Field


class Feedback(BaseModel):
    """User's feedback about Propoe.

    Attributes
    ----------
    stars: int
        Stars evaluation, should be between 1 and 5.
    comment: str
        Comment content, should have the size of a Tweet, 280 characters.
    """

    stars: int = Field(
        examples=["5"], strict=True, ge=1, le=5, description="Stars evaluation"
    )
    comment: str = Field(
        examples=["Excelent, Propoe2 is awesome!"],
        strict=True,
        max_length=280,
        description="Feedback content",
    )
