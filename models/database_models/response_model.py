from pydantic import BaseModel

class ResponseModel(BaseModel):
    """
    Represents a student's response to a question.

    Attributes:
        question_id (int): Reference to the associated question.
        response_text (str): The student's response text.
        identifier (str): A customizable identifier for the response. An example usage would be a student ID.
    """
    question_id: int
    response_text: str
    identifier: str