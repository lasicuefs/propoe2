from pydantic import BaseModel, field_validator


class Feedback(BaseModel):
    """User's feedback about Propoe."""
    stars: int
    comment: str

    @field_validator("stars")
    @classmethod
    def value_must_be_between_1_and_5(cls, value: int) -> int:
        """Must be between 1 and 5."""
        if not 1 <= value <= 5:
            raise ValueError("Stars evaluation must be between 1 and 5.")
        return value
    
    @field_validator("comment")
    @classmethod
    def content_must_be_big_as_a_tweet(cls, value: str) -> str:
        """Must not be bigger than a Tweet."""
        CHARACTER_LIMIT = 280
        if len(value) > CHARACTER_LIMIT:
            raise ValueError(
                f"content must be up to {CHARACTER_LIMIT} characters."
            )
        return value
