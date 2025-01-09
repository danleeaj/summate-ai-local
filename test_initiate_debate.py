from models.prompt_models.query_model import QueryModel
from utils.initiate_debate import initiate_debate

query = QueryModel(rubric_component="Implies repeated resampling, but does not mention explicitly",
                    student_response="Bootstrapping creates a confidence interval of possible lines of best fit. 1) Obtain a sample data set from observation/experiment with replacement. 2) Generate a new randomized data set from the sample data set (step 1) that has the same number of observations. ex: sample has 1000 points, new data set has 1000 based on this. 3) Repeat step 2 multiple times (>10) and determine the line of best fit for each scatter plot. 4) Place these lines on a scatter plot and a range of linear lines should be seen, this will determine if the original line is within the range of a reliable fit (confidence interval of linear model lines)",
                    context="Describe, step-by-step, the process of bootstrapping to estimate the reliability of coefficients fit by a linear model."
                    )

response = initiate_debate(query=query)

print(response.model_dump_json(indent=2))