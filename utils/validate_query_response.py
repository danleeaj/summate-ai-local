# import json
# from ..utils.validate_query_response import validate_query_response
from pydantic import BaseModel

def clean_string(input: str) -> str:
    clean_input = input.strip().strip("```json").strip("```")
    clean_input = clean_input.replace("'", '"').strip()
    return clean_input

def validate_query_response(input:str, model:BaseModel) -> BaseModel:
    clean_response = clean_string(input)
    try:
        parsed_model = model.model_validate_json(json_data=clean_response, strict=True)
        return parsed_model
    except:
        print("Failed to validate JSON")
        return