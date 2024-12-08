from pydantic import BaseModel
from typing import List
from models.response_model import ResponseModel

class RoundModel(BaseModel):
    """
    Represents a single round of a debate, consisting of two Grader and one Evaluator response.

    Attributes:
        responses (list[Response]): A list of three responses from Grader 1, Grader 2 and the Evaluator.
        evaluation_error_flag (bool): Indicates mismatch between the individual Grader's evaluations and the Evaluator's determination of their agreement. For example, the Graders do not agree with each other, however, the Evaluator reports they do agree.
        consensus_error_flag (bool): Indicates mismatch between the Evaluator's consensus evaluation and the individual Grader's evaluations. For example, the Graders agree that the rubric component is satisfied, however, the Evaluator reports that the component was not satisfied.
    """
    responses: List[ResponseModel]
    evaluation_error_flag: bool
    consensus_error_flag: bool