from ollama import chat
from ollama import ChatResponse

from icecream import ic

from typing import List

from utils.llm_models import LLMModel

from pydantic import BaseModel
from models.response_models.grader_response_model import GraderResponseModel
from models.response_models.evaluator_response_model import EvaluatorResponseModel

from utils.validate_query_response import validate_query_response
from utils.message_generation import prompt_to_jsonifier

def query_large_language_model(query: List[BaseModel], model: LLMModel, validation_model: BaseModel) -> EvaluatorResponseModel | GraderResponseModel:
    
    message_list = []

    for message in query:
        json_message = message.model_dump()
        message_list.append(json_message)

    validated_response = None
    tries = 0
    max = 10

    response: ChatResponse = chat(model=model.value, messages=message_list)
    
    message_to_be_jsonified = response.message.content

    ic(message_to_be_jsonified)

    json_message_list = []
    json_message_models = prompt_to_jsonifier(validation_model=validation_model, message_to_be_jsonified=message_to_be_jsonified)

    for message in json_message_models:
        json_message = message.model_dump()
        json_message_list.append(json_message)

    while tries < max and not validated_response:

        print(f"Attempt {tries} to parse JSON")
        json_response: ChatResponse = chat(model=LLMModel.GEMMA.value, messages=json_message_list)
        validated_response = validate_query_response(json_response.message.content, validation_model)
        tries += 1

    if tries == max:
    
        ic("Error in decoding JSON. Expect a downstream validation error.")

    return validated_response