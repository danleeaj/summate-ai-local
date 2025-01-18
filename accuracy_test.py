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

from models.prompt_models.query_model import QueryModel
from pydantic import BaseModel
from utils.initiate_debate import initiate_debate
from utils.old_initiate_debate import old_initiate_debate
from utils.old_initiate_debate import old_initiate_debate

from utils.database_manager import DebateDatabase

from utils.message_generation import initial_prompt_to_grader
from utils.query_large_language_model import query_large_language_model

from utils.old_message_generation import initial_prompt_to_grader as old_prompt

from utils.llm_models import LLMModel

from datetime import datetime

from typing import List

class PlaceholderModel(BaseModel):
    content: int

placeholder = PlaceholderModel(content=0)

question = "Describe, step-by-step, the process of bootstrapping to estimate the reliability of coefficients fit by a linear model."

list = [
    {'id': 1, 'content': 'Bootstrapping creates a confidence interval of possible lines of best fit. 1) Obtain a sample data set from observation/experiment with replacement. 2) Generate a new randomized data set from the sample data set (step 1) that has the same number of observations. ex: sample has 1000 points, new data set has 1000 based on this. 3) Repeat step 2 multiple times (>10) and determine the line of best fit for each scatter plot. 4) Place these lines on a scatter plot and a range of linear lines should be seen, this will determine if the original line is within the range of a reliable fit (confidence interval of linear model lines)', 'score': [1, 1, 1, 1, 1]},
    {'id': 2, 'content': '1. Get a subsample of yoru data. 2. Get a linear regression model of this data. 3. Repeat the process. 4. Find the average of these lines. 5. Indicate the confidence interval of those lines through the shading  […] the regression line.', 'score': [1, 0, 1, 1, 1]},
    {'id': 3, 'content': '1. Sample the true data many times (with replacement) to create multiple (n) synthetic data sets. 2. Based on the samples, calculate the linear coefficients for the. 3. Plot and look at thie distribution of these coefficients. This will provide a confidence interval and estimate reliabilty of coefficients.', 'score': [1, 1, 1, 1, 1]},
    {'id': 4, 'content': 'Bootstrapping involves first random sampling with replacement. It is recommended that that number of samples you take out and replace is equal to the number of data points you have. Next it involves creating a regression line for each of those samples to get an estimate of the line of best fit. Ultimately you would get a confidence interval of the regression line, and where most of the data points lie.', 'score': [1, 1, 0, 1, 1]},
    {'id': 5, 'content': 'Bootstrapping is the process of taking values that lie within reasonable range of the line of best fit, and calculating a level of variance. This gives insight on how reliable the coefficients of the lines average (y = mx + b). Steps of calculating variance: 1. Set parameters to catch values that fall within a specific range or closeness of the line. 2. Find out how neat or scattered this data is and use this conclusion to inform the rest of analysis.', 'score': [0, 0, 0, 0, 1]},
    {'id': 6, 'content': '1. Sample data x number of times, x should be high for confidence. 2. Find regression for each sample best fit line. 3. Combine regressions to get a range of these best fit lines. 4. The narrower the range the more reliable and confident, the wider the range, the less reliable and confident.', 'score': [1, 0, 1, 1, 1]},
    {'id': 7, 'content': '1. Obtain a sample of size n. 2. With replacement, pull multiple samples of size n from the sample. 3. Calculate the correlation coefficients of each bootstrapped sample. 4. Calculate the z-score of the correlation coefficients. If the p-value is high (insignificant), we can theorize that a linear model is reliable.', 'score': [1, 1, 1, 1, 0]},
    {'id': 8, 'content': "Firstly, use the linear model to testify the line fitness. Y = ax + b. If the correlation coefficient is low, it suggests that the line doesn't match with the linear model. As a result, we need to adjust the slope (a) or the intercept (b) to fit the model. If the difference between the mean values and actual values are reliabily small, the model should fit.", 'score': [0, 0, 0, 0, 0]},
    {'id': 9, 'content': 'Bootstrapping can estimate how good of a linear fit your model is. 1. Resample your data randomly from original data set. 2. Make a linear fit of resample. 3. Plot fit alongside the original linear fit model (but with some opacity). 4. Repeat steps 1-3 n number of times, In our class, we said n = 1000 to 2000 is generally good.', 'score': [1, 0, 1, 1, 1]},
    {'id': 10, 'content': '1. From a set of data, take a sampel of that data with replacement. 2. Repeat step 1 multiple times, still with replacement. 3. Find coefficients for each fo your individual samples. 4. Compare the coefficeitns between each of your samples to judge the reliability of your overall correlation of the entire dataset.', 'score': [1, 1, 1, 1, 1]},
    {'id': 11, 'content': 'Involves wrangling data sets in order to normalize the distribution. This involves taking either ends and using the normal distribution formula.', 'score': [0, 0, 0, 0, 0]},
    {'id': 12, 'content': '1. Randomly generates a large sample of data from dataset (usually should be over 1000 samples). 2. For each sample, calculate the descriptive statistics, 3. Plot the bootstrapping data & check correlation & reliability (check r, E, R^2) of the plotted data.', 'score': [1, 0, 0, 1, 1]},
    {'id': 13, 'content': 'Recreate several versions of the sample data by random sampling and replacement. Find the slopes of each version and find the mean slope. Compare this mean slope to the linear model. Apply this with the r and r^2 of the bootstrapped mean and the linear model.', 'score': [1, 1, 1, 1, 0]},
    {'id': 14, 'content': '1. Resample (since there are 5 datapoints, I would resample five times). 2. Create linear model; I would create a new linear model for each sample. 3. Combine models; I would combine these lines to create a new model that illustrates my interval of confidence which will describe how likely it’ll be that a data point falls into that range on the graph.', 'score': [1, 0, 0, 1, 1]},
    {'id': 15, 'content': '1. Bootstrapping takes random small samples from a dataset. 2. Calculate the coefficiens of the small samples. 3. Compare the small samples to the linear model.', 'score': [1, 0, 0, 1, 0]},
    {'id': 16, 'content': 'Bootstrapping is a method of multipile trials. We have an intiial fit to the data. We then refit the data from scratch after selecting a subsample. We fit this new subsamples data and find the mean model for it. We repeat this process a number of times. Evaluate the differences between our linear fits. Choose the most closest fit line.', 'score': [1, 0, 1, 1, 1]},
    {'id': 17, 'content': '1. We calculate the line of best fit (for ex) of our original data set (imagine we have 100 samples. 2. Create 100 false data sets through random sampling with duplicates (a datapoint added more than once) 3. Take the line of best fit (for ex) of all those data sets separately. 4. Compare how reliable our data is based on how much variability there is in the line of best fits collected. 5. We can use bootstrapping to estimate the reliability of coefficients fit by a linear model because we can plot all the lines of best fits onto one graph and determine whether there truly is a correlation in our dataset. The less our variability in all the lines of best fits, the more reliable our data set is and we can make a correlation.', 'score': [1, 1, 1, 1, 1]},
    {'id': 18, 'content': '1. Start off with a data set that has n number of data points. 2. Resample the data n number of times, making a linear model/lines of best fit for each sample (resample). 3. Compile all of the regression lines with will create a confidence interval of the data points to estimate the reliability/fit of the model.', 'score': [1, 0, 1, 1, 1]},
    {'id': 19, 'content': 'Create an array. Plot points in order to observe correlation if any. You run pearson correlation tests and find R^2 value, depending on the data you can have strong or no correlation. You can run statistical analysis and use distribution test depending on the type of data you have.', 'score': [0, 0, 0, 0, 0]},
    {'id': 20, 'content': '1. From the dataset, randomly sample with replacement to create a set of new datasets. 2. Determine the coefficients estimated for each dataset. 3. Create a confidence interval of the coefficients to determine how confident we are that the true coefficient of the linear model is within the range predicted by the generated datasets.', 'score': [1, 1, 1, 1, 1]},
    {'id': 21, 'content': 'Bootstrapping takes a dataset and samples it multipel times with replacement. 1. Take a large dataset, 2. take multiple smaller samples with replacement n number of times, 3. find coefficients for each substample. For example you can', 'score': [1, 1, 1, 1, 0]},
    {'id': 22, 'content': 'First sample random data from dataset to graph the best linear fit line. Then, with replacement, repeat the step above to random sampling from dataset set to generate sufficient amount of linear fit. Combine them together to estimate the coefficients that fit the linear model of the dataset.', 'score': [1, 1, 1, 1, 1]},
    {'id': 23, 'content': 'First generate your linear regression model. Then, randomly sample the points within your distribution to assess the fit of that model to the points. Using this information, repeat this process iteratively until you can verify the robustness & validity of your model.', 'score': [1, 0, 1, 0, 0]},
    {'id': 24, 'content': 'Take a random subsample from the sample. Calculate line of best fit by maximizing R². (Recall R² = 1 - RSS/TSS). TSS is const, so minimize RSS. Plot line on data. Repeat N times, where N = the number of samples. The reason why: a larger spread of lines means greater uncertainty that the line of best fit reflects population trends. (line of best fit is calculated using sample). Cannot directly determine line of best fit of population', 'score': [1, 0, 1, 1, 1]},
    {'id': 25, 'content': 'As shown in the assignment and lecture, Pearson correlation only reflects linear correlation. First, you want to find the equation of the line of best fit. And calculate the residues of the actual data against the line of best fit. Plot the residuals against the x (dependent variable) ad you should see no pattern in the residual plots. Furthermore, the residuals should be randomly distributed and the zero line for a reliable linear model with no skewness. If distinct pattern, skewed distribution is found in the residuals plots. Coefficient is not reliable where you need to look for outlier or other models.', 'score': [0, 0, 0, 0, 0]},
    {'id': 26, 'content': '1. Sample with replacement from the original data (usually take the same number of samples as the number of data points). 2. Calculate new regression coefficients for each of the new samples. 3. Calculate confidence interval for the linear model coefficients based on the distribution of coefficients observed from the above step to determine reliability.', 'score': [1, 1, 0, 1, 1]},
    {'id': 27, 'content': 'First, you would take resamples of the data with replacement, so that you would get more random samples with the limited data that you have. Then, fit a linear regression to each resample, resulting in a number of regression lines. Then, comparing all of the linear regression lines from the resampled data to the coefficients fit by a linear model will allow you to determine its reliability.', 'score': [1, 1, 0, 1, 1]},
    {'id': 28, 'content': 'Randomly resample a certain number of data points from the data available - Repeat the resampling process with replacement to get some subsets of the data. For each subset, fit a linear regression model (potentially using the standards of minimizing MSE or maximizing MLE). The regression models from the last step together make up a range where coefficients would vary in indicating the reliability of fit by a linear model. The coefficients fit by a linear model is more reliable when the fitted lines are closer together (have similar coefficients) [can run statistical tests on these coefficients if necessary]', 'score': [1, 1, 1, 1, 1]},
    {'id': 29, 'content': 'Bootstrapping is a way of assessing fit with one sample. 1. From the original sample (size n), sample with replacementn times (resample size = n) 2. Find an estimate of comparison (in this case, we will determine reliability in the linear model (line of best fit). 3. Repeat steps 1 & 2 to create a distribution of the best fit lines for many resamples. Based on the distribution, if the linear model bootstrap distribution still shows coefficients fit within the interval, then we can say the model is at least some what reliable. If it demonstrated that coefficients fit includes 0, then a linear model may not be the most reliable (indicates weak fitting).', 'score': [1, 1, 1, 1, 1]},
    {'id': 30, 'content': "Given a sample of n points, resample the data n times and with each new sample, fit a linear model. After fitting a linear models on the subsets, a confidence interval will be generated. The reliability of coefficients can be determined by how closely it fits this interval of 'fits'.", 'score': [1, 0, 1, 1, 1]},
    {'id': 31, 'content': '1. Resampling from the original model distribution with replacement for many times. 2. Plot the intercepts and slopes of the generated distributions. 3. Apply 95% confidence interval (or other CI) onto the distributions of the intercepts and slopes separately (and or the int/slope of the original dist). 4. Determine if [...] is covered in the CI. If not, the intercept and/or/ the slope of the original model is meaningful.', 'score': [1, 1, 1, 0, 1]},
    {'id': 32, 'content': 'Bootstrapping starts with finding the equation of the linear model and the R^2 value. Once these values are found, the coefficients of the linear model are transformed by R^2 to create an upper and lower limit for the plotted data. The area around the line of best fit line is shaded and bootstrapped and the best fit linear model fits inside this region. If the line closest fit in the region, then the linear model is not a good estimate of the coefficients.', 'score': [0, 0, 0, 0, 0]},
    {'id': 33, 'content': "Bootstrapping is when you fit a linear regression into a model with an error area/scale around the estimation. First, you find the linear equation best fitted for the data. Then you find the mean standard error of the line around the data. With that it will give you the best line of fit with a 'best confidence' and around the actual data points.", 'score': [0, 0, 0, 0, 0]},
    {'id': 34, 'content': 'Bootstrapping refers to plotting everypoint and then viewing how the line of bets fit looks like. Then some calculations are taken of the data poits to see how close that line of best fit is.', 'score': [0, 0, 0, 0, 0]},
    {'id': 35, 'content': 'Bootstrapping is the process of iteratively fitting linear models to data produce a model of best fit. This is done with replacement so that the data is not being changed. First, a model needs to be created, we can use the simmple function y = theta_0 + theta_x_i + noise. We then check for the error of this model, say by calculating the residuals covariance, R^2... Adjust the model accordingly to reduce the error present.', 'score': [0, 1, 1, 1, 0]},
    {'id': 36, 'content': 'Given a dataset and its correlation plot, bootstrapping involves random sampling with replacement to generate smaller subplots to determine the line of best fit and combine them all back into one. Essentially this accounts for uncertainty in the line of best fit for the complete dataset, the range in which it could slightly vary.', 'score': [1, 1, 0, 1, 1]},
    {'id': 37, 'content': 'Bootstrapping is random sampling using replacement. To use it, you should take samples from your sample data that you would like to model & use regression to access how the sample of samples fits the model. You would repeat this many times without removing previously samples data points & your data will eventually converge in a way that should be representative of the population. Repeatedly using R^2 as a metric for how the data fits the linear model will give you an idea of whether the linear model is representative, because now the sample data will be normal & should converge to the actual values that the model is trying to represent - if there is a reliably high or low R^2 it will say something about the true correlation.', 'score': [1, 1, 1, 1, 0]},
    {'id': 38, 'content': 'So lets say you are plotting data about the amount of hours each student studies for an exam. You can use bootstrapping by taking multiple replaceable trials to estimate the reliability of fit given by each plot generated. Since you are replacing the outcome of each trial you can predict how reliable the plots are and compare them to all the data acquired. The whole point of bootstrapping is that the trials are repeatable and replaceable in your experiment trials.', 'score': [1, 1, 1, 0, 0]},
    {'id': 39, 'content': 'Bootstrapping is essentially taking many random samples from the initial data to see if the linear model is coefficient is reliabe. So first, use np.random, combine to generate many random samples of your initial dataset. Then, set your model = linear regression(), then use model.fit() on your samples. Then , you will plot all of those fits with their residuals (%r2 mean score) on the same plot so you could see if the linear regression fit worked for your random samples.', 'score': [1, 0, 1, 1, 1]},
    {'id': 40, 'content': '1. Take a resampling of an existing sample population. 2. Find the linear regression equation and calculate its R^2 and mean squared error. 3. Repeat #1 and #2 (but each resamples point stays in the sample population so it can be resampled multiple times). 4. Graph all linear regression equations to see density (when the best fit is or find best fit through greatest r^2 and smallest mean square error)', 'score': [1, 1, 1, 1, 1]},
    {'id': 41, 'content': 'Bootstrapping can be done by taking many instances of random samples from a larger population, finding the line of best fit, and repeating until there are many different lines of best fit. These can then be combined to achieve an overall bootstrapping estimate of where the average data points fall. This can then be used to test the reliability of the linear model we are testing, to see if it lies within the expected region.', 'score': [1, 0, 1, 1, 1]},
    {'id': 42, 'content': 'Bootstrapping is done by repeatedly resampling from the original sample (with replacement) to generate many samples from which the means can be calculated. From all these means, we can calculate a confidence interval that gives a range that the actual population mean is likely to be found.', 'score': [1, 1, 1, 0, 1]},
    {'id': 43, 'content': 'Bootstrapping takes multiple different samples from a large dataset and calculates the line of best fit for each subset of data. The visual it produces gives an estimate of how certain we are that the line of best fit represents the data. The thicker (wider) the line is, the more uncertainty there is that it fits the data.', 'score': [1, 0, 1, 1, 1]},
    {'id': 44, 'content': "1. From the true data, randomly select out many synthetic data set. 2. Form estimator using synthetic data set. 3. Using the estimators together, to form a distribution, and inspect the distribution to verify model's confidence/reliability.", 'score': [1, 0, 1, 1, 1]},
    {'id': 45, 'content': '1. Random sampling many circumstance from initial data set. 2. Generate many distribution of those from random sampling. 3. We inspect the distribution of all possible outcomes from the random sampling we get to quantify the confidence interval.', 'score': [1, 0, 0, 0, 1]},
    {'id': 46, 'content': 'No response provided', 'score': [0, 0, 0, 0, 0]},
]

rubric_components = [
    {'id': 1, 'component': 'Resample from data'},
    {'id': 2, 'component': 'Resampling done with replacement'},
    {'id': 3, 'component': 'Take several sets of resamplings'},
    # {'id': 4, 'component': 'Implies repeated resampling, but does not mention explicitly'},
    {'id': 5, 'component': 'Determine the coefficients from the line of best fit for each resampling'},
    # {'id': 50, 'component': 'Calculates a metric from the gathered lines of best fit'},
    # {'id': 6, 'component': 'Mentions calculating a metric from each resampling, but does not specify OR metric calculated from each resampling, but incorrect one'},
    {'id': 7, 'component': 'Gather all lines of best fit to gauge reliability (plot all lines together or plot histogram of coeﬃcients)'},
    # {'id': 8, 'component': 'Mentions comparing coeﬃcients to coeﬃcient for original data'},
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

def consistency_test(repeats, response, component, question, test_name, model: LLMModel):

    db = DebateDatabase(test_name=test_name)

    for i in range(repeats):

        print(f"\nGrading following query ({i+1}/{repeats}):")
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

def consistency_test_old(repeats, response, component, question, test_name, model: LLMModel):

    db = DebateDatabase(test_name=test_name)

    for i in range(repeats):

        print(f"\nGrading following query ({i+1}/{repeats}):")
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

def consistency_test_no_debate(repeats, response, component, question, test_name, model: LLMModel):

    db = DebateDatabase(test_name=test_name)

    for i in range(repeats):

        print(f"\nGrading following query ({i+1}/{repeats}):")
        query = QueryModel(
            rubric_component=component['component'],
            student_response=response['response'],
            context=question
        )
        print(query.model_dump_json(indent=2))

        grader1_start_time = datetime.now()

        grader1_message_list = initial_prompt_to_grader(query)

        grader1_response = query_large_language_model(query=grader1_message_list,
                                                    model=model,
                                                    validation_model=GraderResponseModel)
        
        grader1_response_formatted = ResponseModel(type="Grader",
                                                model=model,
                                                content=grader1_response,
                                                time_requested=grader1_start_time,
                                                time_completed=datetime.now())
        

        print(grader1_response_formatted.model_dump_json(indent=2))

        if grader1_response_formatted:
            match grader1_response_formatted.content.rubricComponentSatisfied:
                case False:
                    int_evaluation = 0
                case True:
                    int_evaluation = 1
                case _:
                    int_evaluation = 2
        else:
            int_evaluation = 3
            grader1_response_formatted = placeholder

        db.add_row((response['id'], component['id'], int_evaluation, model.value, grader1_response_formatted))

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
            
            
def test_matrix_no_debate(responses, components, question, test_name, model: LLMModel):

    db = DebateDatabase(test_name=test_name)

    for response in responses:

        for component in components:

            print(f"\nGrading following query:")
            query = QueryModel(
                rubric_component=component['component'],
                student_response=response['response'],
                context=question
            )
            print(query.model_dump_json(indent=2))

            grader1_start_time = datetime.now()

            grader1_message_list = initial_prompt_to_grader(query)

            grader1_response = query_large_language_model(query=grader1_message_list,
                                                        model=model,
                                                        validation_model=GraderResponseModel)
            
            grader1_response_formatted = ResponseModel(type="Grader",
                                                    model=model,
                                                    content=grader1_response,
                                                    time_requested=grader1_start_time,
                                                    time_completed=datetime.now())
            

            print(grader1_response_formatted.model_dump_json(indent=2))

            if grader1_response_formatted:
                match grader1_response_formatted.content.rubricComponentSatisfied:
                    case False:
                        int_evaluation = 0
                    case True:
                        int_evaluation = 1
                    case _:
                        int_evaluation = 2
            else:
                int_evaluation = 3
                grader1_response_formatted = placeholder

            db.add_row((response['id'], component['id'], int_evaluation, model.value, grader1_response_formatted))
            
def test_matrix_no_debate_old(responses, components, question, test_name, model: LLMModel):

    db = DebateDatabase(test_name=test_name)

    for response in responses:

        for component in components:

            print(f"\nGrading following query:")
            query = QueryModel(
                rubric_component=component['component'],
                student_response=response['response'],
                context=question
            )
            print(query.model_dump_json(indent=2))

            grader1_start_time = datetime.now()

            grader1_message_list = old_prompt(query)

            grader1_response = query_large_language_model(query=grader1_message_list,
                                                        model=model,
                                                        validation_model=GraderResponseModel)
            
            grader1_response_formatted = ResponseModel(type="Grader",
                                                    model=model,
                                                    content=grader1_response,
                                                    time_requested=grader1_start_time,
                                                    time_completed=datetime.now())
            

            print(grader1_response_formatted.model_dump_json(indent=2))

            if grader1_response_formatted:
                match grader1_response_formatted.content.rubricComponentSatisfied:
                    case False:
                        int_evaluation = 0
                    case True:
                        int_evaluation = 1
                    case _:
                        int_evaluation = 2
            else:
                int_evaluation = 3
                grader1_response_formatted = placeholder

            db.add_row((response['id'], component['id'], int_evaluation, model.value, grader1_response_formatted))

def test_matrix_multi(responses, components, question, test_name, model: List[LLMModel]):

    db = DebateDatabase(test_name=test_name)

    grader1_model, grader2_model, evaluator_model = model

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
                    debate = initiate_debate(query=query, grader1_model=grader1_model, grader2_model=grader2_model, evaluator_model=evaluator_model)
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

            db.add_row((response['id'], component['id'], int_evaluation, "placeholder", debate))

if __name__ == "__main__":
    
    # for i in range(5):
    #     test_matrix_no_debate_old(responses, rubric_components, question, f"accuracy_nomad_nothink_gemma9b_{i}", LLMModel.GEMMA)
    
    # test_matrix(list, rubric_components, question, "accuracy_mad_think_gemma9b_orig", LLMModel.GEMMA)
    
    # Test for consistency
    # consistency_test(10, responses[1], rubric_components[6], question, "consistency_mad_think_gemma9b_2_7", LLMModel.GEMMA)
    # consistency_test_no_debate(10, responses[1], rubric_components[6], question, "consistency_nomad_think_gemma9b_2_7", LLMModel.GEMMA)
    # consistency_test(10, responses[2], rubric_components[2], question, "consistency_mad_think_gemma9b_3_3", LLMModel.GEMMA)
    # consistency_test_no_debate(10, responses[2], rubric_components[2], question, "consistency_nomad_think_gemma9b_3_3", LLMModel.GEMMA)
    
    # Test for accuracy for no debate
    
    for i in range(1, 10):
    
        # test_matrix(responses, rubric_components, question, f"accuracy_mad_think_qwen7b_{i}", LLMModel.QWEN2)
        # test_matrix_multi(responses, rubric_components, question, f"accuracy_multi_gemma9b_qwen7b_{i}", [LLMModel.GEMMA, LLMModel.QWEN2, LLMModel.GEMMA])
        # test_matrix(responses, rubric_components, question, f"accuracy_mad_think_gemma9b_{i}", LLMModel.GEMMA)
        # test_matrix(responses, rubric_components, None, f"accuracy_mad_think_gemma9b_noq_{i}", LLMModel.GEMMA)
        # test_matrix_no_debate(responses, rubric_components, question, f"accuracy_nomad_think_gemma9b_{i}", LLMModel.GEMMA)
        test_matrix_old(responses, rubric_components, question, f"accuracy_mad_nothink_gemma9b_{i}", LLMModel.GEMMA)