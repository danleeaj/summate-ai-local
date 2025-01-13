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
                                 content="You are a grading judge tasked with evaluating responses from two grading agents to determine if they truly agree on whether a rubric component is satisfied. You must analyze beyond surface-level agreement and examine their underlying reasoning.")

    user_prompt = MessageModel(role="user",
                               content=f"""
        Analyze these grading evaluations:

        Grader 1: '{grader1response_string}'
        Grader 2: '{grader2response_string}'

        1. IDENTIFY CORE ELEMENTS:
        - What key evidence does each grader cite?
        - What are their main observations about the student's response?
        - What core reasoning leads to their conclusions?

        2. COMPARE FUNDAMENTAL REASONING:
        - Are graders looking at the same evidence?
        - Do they make similar observations about this evidence?
        - Are their reasoning processes compatible or contradictory?

        3. DETERMINE AGREEMENT STATUS:
        Graders AGREE if:
        - They reach the same conclusion using compatible reasoning
        - They identify the same key evidence, even if emphasized differently
        - Their core analysis aligns, even if expressed differently
        - They use different words to describe the same concept or observation

        Graders DISAGREE if:
        - They interpret the same evidence in fundamentally different ways
        - Their core reasoning contradicts each other
        - They focus on completely different aspects of the response
        - They have incompatible standards for evaluation

        NOTE: Different wording or emphasis does NOT constitute disagreement if the underlying analysis is compatible.

        Provide:
        1. Whether the graders fundamentally agree
        2. If they agree, state their consensus evaluation
        3. A clear explanation focused on core reasoning rather than wording differences""")
    
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
                                 content=f"""You are a biology grading assistant. Your task is to evaluate student responses to determine if the rubric component is addressed{', taking into account the information provided to the student in the context section' if context else ''}. 
                                 
                                Key Evaluation Principles:
                                1. Consider both explicit statements AND implicit demonstration of understanding
                                2. Technical concepts can be demonstrated through proper usage, even without detailed explanations
                                3. Focus on evidence that the student understands the core concept, not just their ability to explain it technically""")

    user_prompt = MessageModel(role="user",
                               content=f"""
        The rubric component is: '{rubric_component}'.
        The student response is: '{student_response}'.
        {'The context is: ' + f"'{context}'" if context else ''}

        Your task is to evaluate if the student's response demonstrates understanding of the core concepts in the rubric component. Follow this analysis process:

        1. RUBRIC ANALYSIS:
        - What is the core concept being evaluated?
        - What would demonstrate understanding of this concept?
        - Note any OR conditions that provide multiple valid paths to satisfaction
        - List each possible path to satisfaction separately
        - Remember: Only ONE path needs to be satisfied
        - Example: If rubric says "A or B", student only needs A OR B, not both

        2. RESPONSE ANALYSIS:
        - Quote the EXACT portions of the response that relate to the rubric component

        3. EVIDENCE EVALUATION:
        - Does the student demonstrate understanding through explicit explanation of the concept?
        - Does the evidence match the EXACT level of detail required?
        - Avoid requiring more specificity than the rubric demands

        4. FINAL DETERMINATION:
        Based strictly on the evidence found, determine if the rubric requirements are met.

        Evaluation Guidelines:
        - Require clear, direct evidence for each component
        - Look for specific terminology and clear explanations
        - Do not make assumptions about student knowledge
        - Do not give benefit of doubt for unclear or ambiguous statements

        Your response MUST:
        1. List specific requirements from the rubric
        2. Quote exact evidence from the response
        3. Explain how the evidence matches or doesn't match the requirement
        4. End with "EVALUATION:" followed by Yes/No and specific missing or satisfied elements

        Focus on what is explicitly present in the response, not what might be implied or assumed.""")

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
                               content=f"""The other grader has provided a different evaluation. Please carefully analyze their reasoning and reconsider your position:

        Their evaluation: {opposing_grader_response.rubricComponentSatisfied}
        Their reasoning: {opposing_grader_response.explanation}

        Please re-evaluate following these steps:

        1. ANALYSIS OF OPPOSING VIEW:
        - What specific evidence did they identify that you might have overlooked?
        - What alternative interpretations of the rubric or response did they consider?
        - Are there valid points in their reasoning that deserve consideration?

        2. DEFENSE OR REVISION OF YOUR POSITION:
        - Re-examine the evidence you originally identified
        - Consider if the opposing view changes your interpretation of any evidence
        - Evaluate if any of your initial assumptions need revision

        3. SYNTHESIS AND FINAL DETERMINATION:
        - Weigh both perspectives against the rubric requirements
        - Consider if partial agreement is possible
        - Make a final determination based on the complete analysis

        4. PROVIDE YOUR FINAL EVALUATION:
        - State whether you maintain or revise your original position
        - Explain your reasoning with specific references to both interpretations
        - Address key points of agreement or disagreement with the other grader

        Remember:
        - Focus on evidence and reasoning, not just asserting a position
        - Consider alternative interpretations fairly
        - It's acceptable to maintain your position if warranted, but explain why the opposing view didn't change your analysis
        - It's also acceptable to change your position if the opposing view revealed overlooked evidence or interpretation.""")

    message_chain = [user_prompt]

    return message_chain