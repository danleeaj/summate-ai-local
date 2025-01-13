from pydantic import BaseModel
from typing import Literal, Optional

class EvaluatorResponseModel(BaseModel):
    """
    Represents the response from the evaluator.

    Attributes:
        gradersAgree (bool): Whether the graders agree with each other.
        consensusEvaluation (str): The consensus reached by the graders. This can be either Yes, No or No consensus reached.
        explanation (str): The reasoning behind the evaluation.
    """
    gradersAgree: bool
    consensusEvaluation: Literal['Yes', 'No', 'No consensus reached']
    explanation: str
    thought: Optional[str] = None