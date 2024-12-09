from pydantic import BaseModel
from typing import Optional

class QueryModel(BaseModel):
    """
    Represents the query sent to the debate framework.

    Attributes:
        rubric_component (str): The rubric component the debate is based off of.
        student_response (str): The student response being evaluated.
        context (str): Additional context for the evaluation.
    """
    rubric_component: str
    student_response: str
    context: Optional[str] = None