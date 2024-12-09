from typing import List, Optional
from models.prompt_models.message_model import MessageModel

def add_message(next_message: MessageModel, previous_message: Optional[List[MessageModel]] = None):
    
    chat_history = []

    if previous_message:
        for message in previous_message:
            chat_history.append(message)
    else:
        chat_history.append(next_message)

    return chat_history