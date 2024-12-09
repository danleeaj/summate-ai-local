from typing import List
from models.prompt_models.message_model import MessageModel
from models.prompt_models.query_model import QueryModel
from models.response_models.grader_response_model import GraderResponseModel

def initial_prompt_to_evaluator(grader1response: GraderResponseModel, grader2response: GraderResponseModel) -> List[MessageModel]:
    """
    Returns the prompt to the evaluator.
    
    Args:
    grader1response (GraderResponseModel): The first grader's response.
    grader2response (GraderResponseModel): The second grader's response.

    Returns:
    The follow up prompt in a list (List[MessageModel]).
    """

    grader1response_string = f"My evaluation is {'yes' if grader1response.rubricComponentSatisfied else 'no'}. This is because: {grader1response.explanation}"

    grader2response_string = f"My evaluation is {'yes' if grader2response.rubricComponentSatisfied else 'no'}. This is because: {grader2response.explanation}"

    system_prompt = MessageModel(role="system",
                                 content="You are a grading judge. Your task is to evaluate the grading responses from two grading agents to determine if they agree on whether a rubric component is satisfied by the student response. You will provide your evaluation in JSON format.")

    user_prompt = MessageModel(role="user",
                               content=f"""
        Grader 1 evaluation: '{grader1response_string}'.
        Grader 2 evaluation: '{grader2response_string}'.
        Your job is to compare the evaluations from Grader 1 and Grader 2. If their evaluations on whether the rubric component is satisfied (YES) or not satisfied (NO) are in agreement with each other, then provide their consensus evaluation and say that they agree by evaluating gradersAgree as TRUE.
        To determine if the graders are in agreement, follow these rules:
        1. If both graders provide the same evaluation (YES or NO), they are considered to be in agreement.
        2. If the graders provide different evaluations (one says YES and the other says NO), then they are considered to be in disagreement.
        3. If the graders provide the same evaluations, but for very different reasons, then they are also considered to be in disagreement.
        However, if the two graders disagree in their evaluations (one says YES and the other says NO), then evaluate gradersAgree as FALSE and say 'No consensus reached' for consensusEvaluation.
        Return your evaluation in JSON format with the following keys:
        "gradersAgree" : <true/false>
        "consensusEvaluation": <'Yes'/'No'/'No consensus reached'>
        "explanation" : <A string with a few sentences explaining your reasoning>
        Ensure that the property names are enclosed in double quotes.
        """)
    
    message_chain = [system_prompt, user_prompt]

    return message_chain
    
def initial_prompt_to_grader(query: QueryModel) -> List[MessageModel]:
    """
    Returns the initial prompt to the grader.

    Args:
    query (QueryModel): The user's prompt.

    Returns:
    The follow up prompt in a list (List[MessageModel]).
    """

    rubric_component, student_response = query.rubric_component, query.student_response
    context = query.context if query.context else None

    system_prompt = MessageModel(role="system",
                                 content=f"You are a biology grading assistant. Your task is to evaluate student responses to determine if the rubric component is explicitly addressed{', taking into account the information provided to the student in the context section' if context else ''}, regardless of its factual accuracy. Do not use your own knowledge to judge the correctness of the rubric component or the student's response. Your role is to check if the student's response matches what the rubric asks for, even if the rubric component itself contains inaccuracies. You will provide your evaluation in JSON format.")

    user_prompt = MessageModel(role="user",
                               content=f"""
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
        """)
    
    message_chain = [system_prompt, user_prompt]

    return message_chain

def followup_prompt_to_grader(opposing_grader_response: GraderResponseModel) -> List[MessageModel]:
    """
    Returns the followup prompt for when there is a disagreement between the two graders.

    Args:
    opposing_grader_response (MessageModel): The opposing grader's response.

    Returns:
    The follow up prompt in a list (List[MessageModel]).
    """

    user_prompt = MessageModel(role="user",
                               content=f"The other agent argues '{opposing_grader_response.rubricComponentSatisfied}'. The reason is '{opposing_grader_response.explanation}'. Please reevaluate your answer and give a new reply in the same format, taking into account the guidelines provided earlier about maintaining confidence, acknowledging different perspectives, and avoiding conformity traps. Maintain your original answer if you still believe you were correct.")

    message_chain = [user_prompt]

    return message_chain