from models.prompt_models.query_model import QueryModel
from utils.initiate_debate import initiate_debate
from database_manager import add_debate

from utils.config import connection_dict

import psycopg

# This should evaluate to TRUE. Check with Ashley for this question. Use these questions to test for consistency.
# rubric_id = 5, response_id = 1
query1 = QueryModel(rubric_component="Determine the coefficients from the line of best fit for each resampling",
                    student_response="Bootstrapping creates a confidence interval of possible lines of best fit. 1) Obtain a sample data set from observation/experiment with replacement. 2) Generate a new randomized data set from the sample data set (step 1) that has the same number of observations. ex: sample has 1000 points, new data set has 1000 based on this. 3) Repeat step 2 multiple times (>10) and determine the line of best fit for each scatter plot. 4) Place these lines on a scatter plot and a range of linear lines should be seen, this will determine if the original line is within the range of a reliable fit (confidence interval of linear model lines)",
                    context="Describe, step-by-step, the process of bootstrapping to estimate the reliability of coefficients fit by a linear model."
                    )

# This should evaluate to TRUE.
# rubric_id = 7, response_id = 1
query2 = QueryModel(rubric_component="Gather all lines of best fit to gauge reliability (plot all lines together or plot histogram of coeﬃcients)",
                    student_response="Bootstrapping creates a confidence interval of possible lines of best fit. 1) Obtain a sample data set from observation/experiment with replacement. 2) Generate a new randomized data set from the sample data set (step 1) that has the same number of observations. ex: sample has 1000 points, new data set has 1000 based on this. 3) Repeat step 2 multiple times (>10) and determine the line of best fit for each scatter plot. 4) Place these lines on a scatter plot and a range of linear lines should be seen, this will determine if the original line is within the range of a reliable fit (confidence interval of linear model lines)",
                    context="Describe, step-by-step, the process of bootstrapping to estimate the reliability of coefficients fit by a linear model."
                    )

# This should evaluate to FALSE.
# rubric_id = 2, response_id = 2
query3 = QueryModel(rubric_component="Resampling done with replacement",
                    student_response="1. Get a subsample of your data. 2. Get a linear regression model of this data. 3. Repeat the process. 4. Find the average of these lines. 5. Indicate the confidence interval of those lines through the shading  […] the regression line.",
                    context="Describe, step-by-step, the process of bootstrapping to estimate the reliability of coefficients fit by a linear model."
                    )

for i in range(9):

    response = initiate_debate(query=query1)

    print(response.model_dump_json(indent=2))

    connection_string = " ".join(f"{key}={value}" for key, value in connection_dict.items())

    with psycopg.connect(connection_string) as conn:

        add_debate(
            conn=conn,
            table_id="debates_consistency_mad_q2",
            debate=response,
            response_id=1,
            rubric_id=7,
        )