import json
import re

from pydantic import BaseModel, ValidationError

from icecream import ic

def fix_json_quotes(json_str):
    # Remove extra whitespace first
    json_str = json_str.strip()
    
    # Find the explanation field and escape its internal quotes
    start_idx = json_str.find('"explanation"')
    if start_idx != -1:
        # Find the first quote after the colon
        content_start = json_str.find(':', start_idx) + 1
        # Find the next quote which starts the content
        first_quote = json_str.find('"', content_start)
        # Find the last quote in the string (before the closing brace)
        last_quote = json_str.rfind('"')
        
        # Get the content between the quotes
        content = json_str[first_quote + 1:last_quote]
        
        # Escape the internal quotes
        escaped_content = content.replace('"', '\\"')
        
        # Reconstruct the JSON string
        fixed_json = (
            json_str[:first_quote + 1] + 
            escaped_content + 
            json_str[last_quote:]
        )
        
        return fixed_json
    
    return json_str

def clean_string(input: str) -> str:
    """
    Cleans and parses JSON-like strings into a JSON-parsable format.
    """

    clean_input = input.strip() # Remove all starting and trailing whitespace
    clean_input = clean_input.replace("```json", "").replace("```", "") # Removes markdown if it's there
    clean_input = clean_input.replace("\\\"", "\"") # Replaces \" with "
    clean_input = clean_input.replace("\"\"", "\"") # Replaces potential "" with "
    clean_input = clean_input.strip()

    if not clean_input.startswith("{") and not clean_input.endswith("}"):
        clean_input = "{" + clean_input + "}"

    return clean_input

def validate_query_response(input:str, model:BaseModel) -> BaseModel:

    clean_response = clean_string(input)
    clean_response = fix_json_quotes(clean_response)

    try:
        json_parse = json.dumps(json.loads(clean_response))
        try:
            parsed_model = model.model_validate_json(json_data=json_parse)
            return parsed_model
        except ValidationError as e:
            print("Validation Error:", e)
            print(json_parse)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print()
        print(clean_response)