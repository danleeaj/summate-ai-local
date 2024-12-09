from typing import List, Optional
from models.prompt_models.message_model import MessageModel

def chain_message(next_message: List[MessageModel] | MessageModel, previous_message: Optional[List[MessageModel]] = None):

    return previous_message + next_message