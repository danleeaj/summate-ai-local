from ollama import chat
from ollama import ChatResponse

from icecream import ic

from typing import List

from utils.llm_models import LLMModel

from pydantic import BaseModel
from models.response_models.grader_response_model import GraderResponseModel
from models.response_models.evaluator_response_model import EvaluatorResponseModel

from utils.validate_query_response import validate_query_response

def query_large_language_model(query: List[BaseModel], model: LLMModel, validation_model: BaseModel) -> EvaluatorResponseModel | GraderResponseModel:
    
    message_list = []

    for message in query:
        json_message = message.model_dump()
        message_list.append(json_message)

    validated_response = None
    tries = 0

    while tries < 5 and not validated_response:

        response: ChatResponse = chat(model=model.value, messages=message_list)
        validated_response = validate_query_response(response.message.content, validation_model)
        tries += 1

    return validated_response