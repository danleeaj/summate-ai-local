from typing import List
from models.prompt_models.message_model import MessageModel
from models.prompt_models.query_model import QueryModel
from models.response_models.grader_response_model import GraderResponseModel
from models.response_models.evaluator_response_model import EvaluatorResponseModel

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

        IMPORTANT INSTRUCTIONS:
        1. Your ENTIRE and ONLY output must be the JSON response.
        2. Do NOT write any text before or after the JSON.
        3. Strictly follow the JSON format with the keys: "gradersAgree", "consensusEvaluation", and "explanation".
        4. Ensure the output is valid, parseable JSON.

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
        Your primary task is to determine if the student's response demonstrates understanding of the core concepts in the rubric component, regardless of the exact wording used. Follow these evaluation steps:

        1. First identify the key concepts in the rubric component
        2. Then look for these concepts in the student response, including semantically equivalent expressions
        3. Consider whether the response shows understanding of these concepts, even if expressed differently
        4. Only mark as unsatisfied if the core concepts are truly missing or misunderstood

        Important evaluation guidelines:
        - Focus on conceptual understanding rather than exact wording matches
        - Students may use different terminology to express the same ideas
        - Consider the context of the field when evaluating semantic equivalence
        - Look for evidence of understanding rather than perfect articulation
        - If a concept is implied through a clear description of its implementation or consequences, consider it present

        Examples of semantic equivalence:
        - "Gather all lines" = "Compile all lines" = "Collect all lines" = "Put together all lines"
        - "Gauge reliability" = "Assess reliability" = "Evaluate reliability" = "Determine reliability"
        - "Plot together" = "Display together" = "Show together" = "Visualize together"

        Return your evaluation in JSON format with the following keys:
        "rubricComponentSatisfied": <"Yes"/"No">
        "explanation": <A string explaining your reasoning that references specific parts of both the rubric and response>

        IMPORTANT INSTRUCTIONS:
        1. Your ENTIRE and ONLY output must be the JSON response
        2. Do NOT write any text before or after the JSON
        3. Ensure the output is valid, parseable JSON
        4. Your explanation should explicitly connect parts of the response to the rubric requirements

        Additionally:
        - Maintain a balanced and confident approach
        - Justify your evaluation with specific references to the text
        - If the rubric asks for multiple elements, check for all of them
        - Evaluate based on presence of concepts, not writing quality
        """)

    message_chain = [system_prompt, user_prompt]

    return message_chain

def prompt_to_jsonifier(validation_model, message_to_be_jsonified):

    if validation_model is GraderResponseModel:  # Direct class comparison
        response_type = 'g'
    elif validation_model is EvaluatorResponseModel:
        response_type = 'e'
    else:
        raise TypeError("Validation model is not of GraderResponseModel or EvaluatorResponseModel")

    grader_json_schema = """{
        "rubricComponentSatisfied": <True/False based on Yes/No>,
        "explanation": <structured reasoning outlining the key evidence found, the grader's interpretation of this evidence, and the decision based on this evidence>
    }
"""

    evaluator_json_schema = """{
        "gradersAgree": <True/False>,
        "consensusEvaluation": <'Yes'/'No'/'No consensus reached'>,
        "explanation": <concise summary of key reasoning>
    """

    schema = grader_json_schema if response_type == 'g' else evaluator_json_schema

    system_prompt = MessageModel(role="system", 
                               content=f"""
                            You are a JSON formatter. Your task is to convert a detailed grading analysis into a standardized JSON response.
                
                            The input will contain a complete analysis followed by a final evaluation. Your job is to:
                            1. Identify the final Yes/No determination
                            2. Extract the key reasoning from the analysis
                            3. Format these into valid JSON

                            Rules for JSON creation:
                            1. Only include the final determination, not intermediate thoughts
                            2. Summarize the key reasoning in 2-3 clear sentences
                            3. Format the response exactly as:

                            {schema}
            
                            Format requirements:
            
                            - Use exact property names as shown
                            - Use true/false (not "true"/"false" or Yes/No)
                            - Keep explanation clear and concise
                            - Ensure valid JSON syntax by using double quotes for all strings
                            - Property names and string values must use double quotes, not single quotes
                            - ALL other occurances of double quotes should be in single quotes
                            - AGAIN: DO NOT HAVE DOUBLE QUOTES WITHIN THE JSON FIELDS.
                            - Do not include any other fields
                            - Do not include any text before or after the JSON
                            - Format must be strictly valid JSON that could be parsed by json.loads()
                
                            Example of correct string formatting:
                            {{
                                "propertyName": "This is a properly formatted string value"
                            }}

                            Example of incorrect string formatting:
                            {{
                                'propertyName': 'This uses invalid single quotes'
                            }}
                            """)
    
    user_prompt = MessageModel(role="user",
                             content=f"""Format this text into JSON according to the schema:

{message_to_be_jsonified}""")
    
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
                               content=f"The other agent argues '{opposing_grader_response.rubricComponentSatisfied}'. The reason is '{opposing_grader_response.explanation}'. Please reevaluate your answer and give a new reply in the same format, taking into account the guidelines provided earlier about maintaining confidence, acknowledging different perspectives, and avoiding conformity traps. Maintain your original answer if you still believe you were correct. Please ensure you are still responding on the same JSON format as specified previously.")

    message_chain = [user_prompt]

    message_chain = [user_prompt]

    return message_chain