from models.prompt_models.query_model import QueryModel
from utils.initiate_debate import initiate_debate

# from database_manager import add_question

test_query = QueryModel(
    rubric_component="Response implies that -1 indicates a perfect negative linear relationship",
    student_response="Pearson correlation coefficient (r) provides the correlation between two variables, ranges between -1 and +1. If r value is >0, there is a positive correlation between two variables. If r value is <0, there is a negative correlation between two variables. It is calculated by the following formula. The closer the value is to 1, regardless of positive or negative, the stronger the correlation. r_xy = (x_c * y_c) / ||x_c||||y_c||, where x_c*y_c is the dot product of two vectors, ||x_c||||y_c|| is the product of the magnitude of two vectors, and the pearson correlation efficient equals: dot product of two vectors divided by the product of magnitude of two vectors.",
    context="Explain the Pearson correlation coefficient (r) in terms of: a. What insights it can provide about data and how to interpret it."
)
