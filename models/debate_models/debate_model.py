from pydantic import BaseModel
from typing import List
from models.debate_models.round_model import RoundModel
from models.prompt_models.query_model import QueryModel

class DebateModel(BaseModel):
    """
    Represents a complete debate process for a specific student response based on a rubric component.

    Attributes:
        evaluation (bool): The final verdict on whether the rubric component is satisfied.
        flagged (bool): Indicates potential error in evaluator evaluation.
        query (Query): The query sent to the debate framework.
        round_count (int): The number of rounds that took place.
        rounds (list[Round]): A list of all rounds of debate that took place.
    """
    evaluation: bool
    flagged: bool
    query: QueryModel
    round_count: int
    rounds: List[RoundModel]