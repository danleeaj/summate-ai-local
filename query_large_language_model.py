from ollama import chat
from ollama import ChatResponse

import time

from models.query_model import QueryModel
from utils.llm_models import LLMModel

test_query = QueryModel(
    rubric_component="Name is stated.",
    student_response="Hi, I'm a neurobiology major.",
)

def query_large_language_model(query: QueryModel, model: LLMModel):

    rubric_component, student_response, context = query.rubric_component, query.student_response, query.context

    test_message_response: ChatResponse = chat(model=model.value, messages=[
        {
			"role": "system",
			"content": f"You are a biology grading assistant. Your task is to evaluate student responses to determine if the rubric component is explicitly addressed{', taking into account the information provided to the student in the context section' if context else ''}, regardless of its factual accuracy. Do not use your own knowledge to judge the correctness of the rubric component or the student's response. Your role is to check if the student's response matches what the rubric asks for, even if the rubric component itself contains inaccuracies. You will provide your evaluation in JSON format.",
        },
        {
            "role": "user",
            "content": f"""
                The rubric component is: '{rubric_component}'.
                The student response is: '{student_response}'.
                {'The context is: ' + f"'{context}'" if context else ''}
                Your job is to carefully read the response and determine if it explicitly addresses the rubric component as stated, regardless of whether the rubric component or the response is factually correct. If there are no relevant responses, indicate that as well.
                Return your evaluation in JSON format with the following keys:
                "rubricComponentSatisfied": <'Yes'/'No'>
                "explanation": <A string with a few sentences explaining your reasoning>
                Ensure that the property names are enclosed in double quotes.
                Additionally, please consider the following when evaluating the response:
                * Maintain a balanced and confident approach, acknowledging the validity of different perspectives without becoming overly conforming.
                * Justify your evaluation with sound reasoning to avoid getting trapped in an endless feedback loop of contradictory arguments.
                * Express any uncertainty or request clarification if needed, rather than simply flipping to the opposing view.
                * Focus solely on whether the student's response matches what the rubric component asks for, even if either the rubric or the response contains factual inaccuracies.
                * Do not use your own knowledge to judge the correctness of the information provided.
                * If the rubric component asks for a specific statement or concept, check if the student's response includes that exact statement or concept, regardless of its accuracy.
                """
        }
    ])

    return test_message_response.message.content
