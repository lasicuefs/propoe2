from pydantic import BaseModel, field_validator


class Stars(BaseModel):
    """User's evaluation of Propoe that goes into ``Feedback``."""
    value: int

    @field_validator("value")
    @classmethod
    def value_must_be_between_1_and_5(cls, value: int) -> int:
        """``value`` must be between 1 and 5."""
        if not 1 <= value <= 5:
            raise ValueError("Stars evaluation must be between 1 and 5.")
        return value


class Comment(BaseModel):
    """User's comment that goes into a ``Feedback``"""
    content: str

    @field_validator("content")
    @classmethod
    def content_must_be_big_as_a_tweet(cls, value: str) -> str:
        """``content`` must not be bigger than a Tweet."""
        CHARACTER_LIMIT = 280
        if len(value) > CHARACTER_LIMIT:
            raise ValueError(
                f"content must be up to {CHARACTER_LIMIT} characters."
            )
        return value


class Feedback(BaseModel):
    """User's feedback about Propoe."""
    stars: Stars
    comment: Comment
