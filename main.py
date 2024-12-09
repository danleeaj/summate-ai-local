from models.prompt_models.query_model import QueryModel
from utils.llm_models import LLMModel

from models.response_models.grader_response_model import GraderResponseModel

from utils.validate_query_response import validate_query_response

from utils.query_large_language_model import query_large_language_model
from utils.message_generation import initial_prompt_to_grader

test_query = QueryModel(
    rubric_component="Name is stated.",
    student_response="Hi, I'm majoring in neurobiology.",
)

response = query_large_language_model(query=initial_prompt_to_grader(test_query), model=LLMModel.GEMMA, validation_model=GraderResponseModel)
print(response)