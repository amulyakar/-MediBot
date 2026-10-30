
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Defines the format of a question
    submitted by the user.
    """

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Medical information question"
    )


class AnswerResponse(BaseModel):
    """
    Defines the format of MediBot's response.
    """

    question: str
    answer: str
    disclaimer: str
