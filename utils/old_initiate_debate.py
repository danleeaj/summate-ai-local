from models.prompt_models.query_model import QueryModel
from utils.llm_models import LLMModel

from models.response_models.grader_response_model import GraderResponseModel
from models.response_models.evaluator_response_model import EvaluatorResponseModel

from utils.validate_query_response import validate_query_response

from utils.query_large_language_model import query_large_language_model
from utils.old_message_generation import initial_prompt_to_grader, initial_prompt_to_evaluator, followup_prompt_to_grader

from models.debate_models.debate_model import DebateModel
from models.debate_models.response_model import ResponseModel
from models.debate_models.round_model import RoundModel

from datetime import datetime, timedelta

from icecream import ic

def old_initiate_debate(query: QueryModel, grader1_model: LLMModel = LLMModel.GEMMA, grader2_model: LLMModel = LLMModel.GEMMA, evaluator_model: LLMModel = LLMModel.GEMMA) -> DebateModel:

    grader1_message_list = initial_prompt_to_grader(query)
    grader2_message_list = initial_prompt_to_grader(query)
    round_list = []

    consensus_reached = False

    while not consensus_reached:

        ic(f"Round {len(round_list) + 1} initiated.")

        grader1_start_time = datetime.now()

        ic("Grader 1 is thinking.")

        grader1_response = query_large_language_model(query=grader1_message_list,
                                                    model=grader1_model,
                                                    validation_model=GraderResponseModel)

        ic("Grader 1 response is received.")

        grader1_response_formatted = ResponseModel(type="Grader",
                                                model=grader1_model,
                                                content=grader1_response,
                                                time_requested=grader1_start_time,
                                                time_completed=datetime.now())
        
        ic("Grader 1 response is formatted.")

        grader2_start_time = datetime.now()

        ic("Grader 2 is thinking.")
        
        grader2_response = query_large_language_model(query=grader2_message_list,
                                                    model=grader2_model,
                                                    validation_model=GraderResponseModel)
        
        ic("Grader 2 response is received.")

        grader2_response_formatted = ResponseModel(type="Grader",
                                                model=grader2_model,
                                                content=grader2_response,
                                                time_requested=grader2_start_time,
                                                time_completed=datetime.now())
        
        ic("Grader 2 response has been formatted.")

        evaluator_start_time = datetime.now()

        ic("Evaluator is thinking.")

        evaluator_response = query_large_language_model(query=initial_prompt_to_evaluator(grader1_response, grader2_response),
                                                        model=evaluator_model,
                                                        validation_model=EvaluatorResponseModel)
        
        ic("Evaluator response has been received.")

        evaluator_response_formatted = ResponseModel(type="Evaluator",
                                                    model=evaluator_model,
                                                    content=evaluator_response,
                                                    time_requested=evaluator_start_time,
                                                    time_completed=datetime.now())
        
        ic("Evaluator response has been formatted.")
        
        round_formatted = RoundModel(responses=[grader1_response_formatted, grader2_response_formatted, evaluator_response_formatted])

        round_list.append(round_formatted)

        grader1_message_list = grader1_message_list + followup_prompt_to_grader(opposing_grader_response=grader2_response)
        grader2_message_list = grader2_message_list + followup_prompt_to_grader(opposing_grader_response=grader1_response)

        consensus_reached = evaluator_response.gradersAgree

        if not consensus_reached:
            ic("Consensus has not been reached, starting next round of debate.")

    ic("Consensus has been reached.")

    debate_formatted = DebateModel(evaluation=evaluator_response.consensusEvaluation,
                                   query=query,
                                   round_count=len(round_list),
                                   rounds=round_list
                                   )
    
    ic("Debate has been formatted.")

    ic(f"The evaluation is: {debate_formatted.evaluation}")
    
    return debate_formatted