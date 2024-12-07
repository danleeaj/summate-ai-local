from pydantic import BaseModel
import pytest
from utils.validate_query_response import validate_query_response

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

def test_json_with_markdown():
    result = validate_query_response(input=json_with_markdown_sample, model=TestModel)
    assert result.response == "Hello!"

def test_json_witout_markdown():
    result = validate_query_response(input=json_without_markdown_sample, model=TestModel)
    assert result.response == "Hello!"

def test_json_without_whitespace():
    result = validate_query_response(input=json_without_whitespace_sample, model=TestModel)
    assert result.response == "Hello!"