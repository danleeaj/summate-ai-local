from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'This is a test message. Just respond with hi!',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)