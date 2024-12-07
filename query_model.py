from ollama import chat
from ollama import ChatResponse

from utils.models import Model

def query_model(query: str, model: Model):

    test_message_response: ChatResponse = chat(model=model.value, messages=[
        {
            'role': 'user',
            'content': query
        }
    ])

    return test_message_response['message']['content']