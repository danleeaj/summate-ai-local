from pydantic import BaseModel

class QuestionModel(BaseModel):
    """
    Represents a question in the database.

    Attributes:
        question_title (str): The title of the question.
        question_text (str): The full text content of the question.
    """
    question_title: str
    question_text: str