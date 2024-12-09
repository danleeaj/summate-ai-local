import json
import re

from pydantic import BaseModel, ValidationError

from icecream import ic

def clean_string(input: str) -> str:
    """
    Cleans and parses JSON-like strings into a JSON-parsable format.
    """

    test_value = "Hello"
    ic(test_value)

    ic(input)

    clean_input = input.strip() # Remove all starting and trailing whitespace
    ic(clean_input)
    clean_input = clean_input.replace("```json", "").replace("```", "") # Removes markdown if it's there
    ic(clean_input)

    clean_input = clean_input.replace("\\\"", "\"") # Replaces \" with "
    ic(clean_input)

    clean_input = clean_input.replace("\"\"", "\"") # Replaces potential "" with "
    ic(clean_input)

    clean_input = clean_input.strip()

    if not clean_input.startswith("{") and not clean_input.endswith("}"):
        clean_input = "{" + clean_input + "}"

    ic(clean_input)
    print(clean_input)
    print()

    return clean_input

def validate_query_response(input:str, model:BaseModel) -> BaseModel:
    clean_response = clean_string(input)

    try:
        parsed_model = model.model_validate_json(json_data=clean_response)
        return parsed_model
    except ValidationError as e:
        print("Validation Error:", e)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
    except Exception as e:
        print("Unexpected Error:", e)