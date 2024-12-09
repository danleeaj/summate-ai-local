from pydantic import BaseModel

class MessageModel(BaseModel):
    """
    Represents a prompt.

    Attributes:
        role (str): The role of the sender, usually 'user', 'system' or 'model'.
        content (str): The content of the message.
    """
    role: str
    content: str