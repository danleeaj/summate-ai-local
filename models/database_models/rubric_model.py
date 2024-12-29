from pydantic import BaseModel
from typing import Optional

class RubricModel(BaseModel):
    """
    Represents a rubric component for evaluating responses.

    Attributes:
        score (Optional[int]): The score for the rubric component.
        component_text (str): The text describing the rubric component.
    """
    score: Optional[int]
    component_text: str