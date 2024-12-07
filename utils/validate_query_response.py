# import json
# from ..utils.validate_query_response import validate_query_response
from pydantic import BaseModel

class TestModel(BaseModel):
    response: str

json_with_markdown_sample = """
```json
{
    'response': 'Hello!'
}
```
"""

json_without_markdown_sample = """
{
    'response': 'Hello!'
}
"""

json_without_whitespace_sample = "{'response': 'Hello!'}"

def clean_string_input(input: str) -> str:
    clean_input = input.strip().strip("```json").strip("```")
    clean_input = clean_input.replace("'", '"').strip()
    return clean_input

def validate_input(input:str, model:BaseModel) -> dict:
    try:
        parsed_input = model.model_validate_json(json_data=input, strict=True)
        return parsed_input
    except:
        print("Failed to validate JSON")
        return
