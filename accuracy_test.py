from models.prompt_models.query_model import QueryModel
from pydantic import BaseModel
from utils.initiate_debate import initiate_debate
from utils.old_initiate_debate import old_initiate_debate

from utils.database_manager import DebateDatabase

from utils.llm_models import LLMModel

class PlaceholderModel(BaseModel):
    content: int

placeholder = PlaceholderModel(content=0)

question = "Describe, step-by-step, the process of bootstrapping to estimate the reliability of coefficients fit by a linear model."

rubric_components = [
    {'id': 1, 'component': 'Resample from data'},
    {'id': 2, 'component': 'Resampling done with replacement'},
    {'id': 3, 'component': 'Take several sets of resamplings'},
    {'id': 4, 'component': 'Implies repeated resampling, but does not mention explicitly'},
    {'id': 5, 'component': 'Determine the coefficients from the line of best fit for each resampling'},
    {'id': 6, 'component': 'Mentions calculating a metric from each resampling, but does not specify OR metric calculated from each resampling, but incorrect one'},
    {'id': 7, 'component': 'Gather all lines of best fit to gauge reliability (plot all lines together or plot histogram of coeﬃcients)'},
    {'id': 8, 'component': 'Mentions comparing coeﬃcients to coeﬃcient for original data'},
]

rubric_components_new = [
    {'id': 1, 'component': "Response indicates that samples are taken from the original dataset (resample)"},
    {'id': 2, 'component': "Response conveys that the resampling is performed with replacement"},
    {'id': 3, 'component': "Response states that the resampling process is performed multiple times to create multiple datasets"},
    {'id': 4, 'component': "Response implies repeated resampling, but fails to state it explicitly"},
    {'id': 5, 'component': "Response indicates that coefficients are determined from the line of best fit of each resampling"},
    {'id': 6, 'component': "Response mentions calculating a metric from each resampled dataset, but is either not the coefficient, or is not specified"},
    {'id': 7, 'component': "Response conveys that all lines of best fit are gathered to gauge reliability either by plotting all lines together or by plotting a histogram of coefficients"},
    {'id': 8, 'component': "Response mentions comparing the new coefficients to the coefficient of the original data"}
]

responses = [
    {'id': 1, 'response': "Bootstrapping creates a confidence interval of possible lines of best fit. 1) Obtain a sample data set from observation/experiment with replacement. 2) Generate a new randomized data set from the sample data set (step 1) that has the same number of observations. ex: sample has 1000 points, new data set has 1000 based on this. 3) Repeat step 2 multiple times (>10) and determine the line of best fit for each scatter plot. 4) Place these lines on a scatter plot and a range of linear lines should be seen, this will determine if the original line is within the range of a reliable fit (confidence interval of linear model lines)", 'score': [1, 1, 1, 0, 1, 0, 1, 0]},
    {'id': 2, 'response': "1. Resample (since there are 5 datapoints, I would resample five times). 2. Create linear model; I would create a new linear model for each sample. 3. Combine models; I would combine these lines to create a new model that illustrates my interval of confidence which will describe how likely it’ll be that a data point falls into that range on the graph.", 'score': [1, 0, 0, 1, 1, 0, 1, 0]},
    {'id': 3, 'response': "Bootstrapping involves first random sampling with replacement. It is recommended that that number of samples you take out and replace is equal to the number of data points you have. Next it involves creating a regression line for each of those samples to get an estimate of the line of best fit. Ultimately you would get a confidence interval of the regression line, and where most of the data points lie.", 'score': [1, 1, 0, 1, 1, 0, 1, 0]},
    {'id': 4, 'response': "Bootstrapping starts with finding the equation of the linear model and the R^2 value. Once these values are found, the coefficients of the linear model are transformed by R^2 to create an upper and lower limit for the plotted data. The area around the line of best fit line is shaded and bootstrapped and the best fit linear model fits inside this region. If the line closest fit in the region, then the linear model is not a good estimate of the coefficients.", 'score': [0, 0, 0, 0, 0, 0, 0, 0]},
    {'id': 5, 'response': "So lets say you are plotting data about the amount of hours each student studies for an exam. You can use bootstrapping by taking multiple replaceable trials to estimate the reliability of fit given by each plot generated. Since you are replacing the outcome of each trial you can predict how reliable the plots are and compare them to all the data acquired. The whole point of bootstrapping is that the trials are repeatable and replaceable in your experiment trials.", 'score': [1, 1, 1, 0, 0, 0, 0, 1]},
]

MAX_RETRIES = 3

def test_matrix(responses, components, question, test_name, model: LLMModel):

    db = DebateDatabase(test_name=test_name)

    for response in responses:

        for component in components:

            print("\nGrading following query:")
            query = QueryModel(
                rubric_component=component['component'],
                student_response=response['response'],
                context=question
            )
            print(query.model_dump_json(indent=2))

            debate = None
            retry_count = 0

            while not debate and retry_count < MAX_RETRIES:
                try:
                    debate = initiate_debate(query=query, grader1_model=model, grader2_model=model, evaluator_model=model)
                except Exception as e:
                    print(f"Error in debate: {e}")
                    retry_count += 1

            if not debate and retry_count == MAX_RETRIES:
                print(f"Failed to initiate debate after {MAX_RETRIES} attempts")

            if debate:
                match debate.evaluation:
                    case "Yes":
                        int_evaluation = 1
                    case "No":
                        int_evaluation = 0
                    case _:
                        int_evaluation = 2
            else:
                int_evaluation = 3
                debate = placeholder

            db.add_row((response['id'], component['id'], int_evaluation, model.value, debate))

def test_matrix_old(responses, components, question, test_name, model: LLMModel):

    db = DebateDatabase(test_name=test_name)

    for response in responses:

        for component in components:

            print("\nGrading following query:")
            query = QueryModel(
                rubric_component=component['component'],
                student_response=response['response'],
                context=question
            )
            print(query.model_dump_json(indent=2))

            debate = None
            retry_count = 0

            while not debate and retry_count < MAX_RETRIES:
                try:
                    debate = old_initiate_debate(query=query, grader1_model=model, grader2_model=model, evaluator_model=model)
                except Exception as e:
                    print(f"Error in debate: {e}")
                    retry_count += 1

            if not debate and retry_count == MAX_RETRIES:
                print(f"Failed to initiate debate after {MAX_RETRIES} attempts")

            if debate:
                match debate.evaluation:
                    case "Yes":
                        int_evaluation = 1
                    case "No":
                        int_evaluation = 0
                    case _:
                        int_evaluation = 2
            else:
                int_evaluation = 3
                debate = placeholder

            db.add_row((response['id'], component['id'], int_evaluation, model.value, debate))

if __name__ == "__main__":
    test_matrix(responses, rubric_components, None, "accuracy_mad_think_gemma9b_orig", LLMModel.GEMMA)
    test_matrix(responses, rubric_components_new, None, "accuracy_mad_think_gemma9b_new", LLMModel.GEMMA)
    test_matrix_old(responses, rubric_components, None, "accuracy_mad_nothink_gemma9b_orig", LLMModel.GEMMA)