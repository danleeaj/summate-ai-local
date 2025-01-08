import pytest
from utils.query_large_language_model import query_large_language_model
from utils.llm_models import LLMModel
from models.prompt_models.message_model import MessageModel
from pydantic import BaseModel

class SimpleResponseModel(BaseModel):
    response: str

def test_query_llm():
    # Create a simple test message
    test_message = MessageModel(
        role="user",
        content="Please respond with a JSON in this format: {\"response\": \"Hello World\"}"
    )
    
    # Call the function with our test message
    response = query_large_language_model(
        query=[test_message],
        model=LLMModel.GEMMA,
        validation_model=SimpleResponseModel
    )

    assert response is not None # Response is received
    assert hasattr(response, 'response') # Response has response attribute
    assert isinstance(response.response, str) # Response is a string

if __name__ == "__main__":
    test_query_llm()