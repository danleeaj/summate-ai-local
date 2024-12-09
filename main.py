from models.prompt_models.query_model import QueryModel
from utils.initiate_debate import initiate_debate

test_query = QueryModel(
    rubric_component="Name is stated.",
    student_response="Hi, I'm majoring in neurobiology.",
)

print(initiate_debate(test_query).model_dump_json(indent=2))