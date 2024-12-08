from pydantic import BaseModel

class GraderResponseModel(BaseModel):
    """
    Represents the response from the grader.

    Attributes:
        rubricComponentSatisfied (bool): Whether the rubric component is satisfied.
        explanation (str): The reasoning behind the evaluation.
    """
    rubricComponentSatisfied: bool
    explanation: str