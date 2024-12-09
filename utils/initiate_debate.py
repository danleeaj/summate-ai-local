from models.prompt_models.query_model import QueryModel
from utils.llm_models import LLMModel

from models.response_models.grader_response_model import GraderResponseModel
from models.response_models.evaluator_response_model import EvaluatorResponseModel

from utils.validate_query_response import validate_query_response

from utils.query_large_language_model import query_large_language_model
from utils.message_generation import initial_prompt_to_grader, initial_prompt_to_evaluator, followup_prompt_to_grader

from models.debate_models.debate_model import DebateModel
from models.debate_models.response_model import ResponseModel
from models.debate_models.round_model import RoundModel

from utils.prompt_chaining import chain_message

from datetime import datetime, timedelta

from icecream import ic

def initiate_debate(query: QueryModel) -> DebateModel:

    grader1_message_list = initial_prompt_to_grader(query)
    grader2_message_list = initial_prompt_to_grader(query)
    round_list = []

    consensus_reached = False

    while not consensus_reached:

        ic(f"Round {len(round_list) + 1} initiated.")

        grader1_start_time = datetime.now()

        grader1_response = query_large_language_model(query=grader1_message_list,
                                                    model=LLMModel.LLAMA,
                                                    validation_model=GraderResponseModel)
        
        grader1_response_formatted = ResponseModel(type="Grader",
                                                model=LLMModel.GEMMA,
                                                content=grader1_response,
                                                time_requested=grader1_start_time,
                                                time_completed=datetime.now())
        
        ic("Grader 1 response has been received.")

        grader2_start_time = datetime.now()
        
        grader2_response = query_large_language_model(query=grader2_message_list,
                                                    model=LLMModel.GEMMA,
                                                    validation_model=GraderResponseModel)

        grader2_response_formatted = ResponseModel(type="Grader",
                                                model=LLMModel.GEMMA,
                                                content=grader2_response,
                                                time_requested=grader2_start_time,
                                                time_completed=datetime.now())
        
        ic("Grader 2 response has been received.")

        evaluator_start_time = datetime.now()

        evaluator_response = query_large_language_model(query=initial_prompt_to_evaluator(grader1_response, grader2_response),
                                                        model=LLMModel.GEMMA,
                                                        validation_model=EvaluatorResponseModel)

        evaluator_response_formatted = ResponseModel(type="Evaluator",
                                                    model=LLMModel.GEMMA,
                                                    content=evaluator_response,
                                                    time_requested=evaluator_start_time,
                                                    time_completed=datetime.now())
        
        round_formatted = RoundModel(responses=[grader1_response_formatted, grader2_response_formatted, evaluator_response_formatted])

        round_list.append(round_formatted)

        grader1_message_list = grader1_message_list + followup_prompt_to_grader(opposing_grader_response=grader2_response)
        grader2_message_list = grader2_message_list + followup_prompt_to_grader(opposing_grader_response=grader1_response)

        consensus_reached = evaluator_response.gradersAgree

    debate_formatted = DebateModel(evaluation=evaluator_response.consensusEvaluation,
                                   query=query,
                                   round_count=len(round_list),
                                   rounds=round_list
                                   )

    ic(f"The evaluation is: {debate_formatted.evaluation}")
    
    return debate_formatted