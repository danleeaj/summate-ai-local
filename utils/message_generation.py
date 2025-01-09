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
        Please analyze these two grading evaluations:

        Grader 1: '{grader1response_string}'
        Grader 2: '{grader2response_string}'

        Conduct your analysis through these steps:

        1. SURFACE ANALYSIS:
        - Document the yes/no determinations from each grader
        - Note immediate apparent agreement or disagreement
        - Identify key phrases and reasoning from each grader

        2. REASONING COMPARISON:
        - Break down each grader's core arguments
        - Identify specific evidence they cited
        - Compare their interpretation of key concepts
        - Look for overlapping or contradicting logic

        3. DEPTH OF AGREEMENT ANALYSIS:
        - Evaluate if graders used similar criteria even if reaching different conclusions
        - Check if same conclusions were reached using contradictory reasoning
        - Assess if graders are interpreting the rubric component similarly
        - Consider if their disagreement is substantive or terminological

        4. CONSENSUS EVALUATION:
        - Determine if there is true agreement in both conclusion AND reasoning
        - If conclusions differ, assess if the disagreement is fundamental
        - If reasoning differs but conclusions match, evaluate if this constitutes true agreement
        - Consider if differences in interpretation are significant enough to nullify surface agreement

        Remember:
        - True agreement requires alignment in both conclusion and underlying reasoning
        - Surface agreement with contradictory reasoning should be treated as disagreement
        - Different terminology expressing the same concept should be recognized as agreement
        - Focus on substantive differences rather than stylistic ones

        After your analysis, provide:
        1. Whether the graders truly agree (considering both conclusion and reasoning)
        2. The consensus evaluation (Yes/No/No consensus reached)
        3. A clear explanation of your determination referencing specific aspects of both responses
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
                                 content=f"You are a biology grading assistant. Your task is to evaluate student responses to determine if the rubric component is explicitly addressed{', taking into account the information provided to the student in the context section' if context else ''}, regardless of its factual accuracy. Do not use your own knowledge to judge the correctness of the rubric component or the student's response. Your role is to check if the student's response matches what the rubric asks for, even if the rubric component itself contains inaccuracies.")

    user_prompt = MessageModel(role="user",
                               content=f"""
        The rubric component is: '{rubric_component}'.
        The student response is: '{student_response}'.
        {'The context is: ' + f"'{context}'" if context else ''}

        Your task is to evaluate if the student's response demonstrates understanding of the core concepts in the rubric component. Walk through your analysis step by step:

        1. ANALYSIS OF RUBRIC:
        - Break down the key concepts and requirements from the rubric component
        - What are the essential ideas that must be demonstrated?

        2. ANALYSIS OF RESPONSE:
        - Identify relevant portions of the student's response
        - Look for both direct statements and implied understanding
        - Consider alternative phrasings and terminology that convey the same concepts

        3. EVIDENCE EVALUATION:
        - Match concepts from the rubric to evidence in the response
        - Consider semantic equivalence and contextual meaning
        - Note any missing or misunderstood concepts
        - Assess if implied or indirect demonstrations of knowledge are sufficient

        4. FINAL DETERMINATION:
        After completing your analysis, provide your final evaluation of whether the rubric component is satisfied.

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

        Your response MUST:
        1. Show your complete thought process through steps 1-3
        2. Only provide your final determination (satisfied/unsatisfied) AFTER showing this analysis
        3. End with the word "EVALUATION:" followed by your clear Yes/No determination and brief summary of why

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
        "explanation": <concise summary of key reasoning>
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
                               - Ensure valid JSON syntax
                               - Do not include any other fields
                               - Do not include any text before or after the JSON
                 
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