# from models.prompt_models.query_model import QueryModel
# from utils.initiate_debate import initiate_debate

# # from database_manager import add_question

# test_query = QueryModel(
#     rubric_component="Response implies that -1 indicates a perfect negative linear relationship",
#     student_response="Pearson correlation coefficient (r) provides the correlation between two variables, ranges between -1 and +1. If r value is >0, there is a positive correlation between two variables. If r value is <0, there is a negative correlation between two variables. It is calculated by the following formula. The closer the value is to 1, regardless of positive or negative, the stronger the correlation. r_xy = (x_c * y_c) / ||x_c||||y_c||, where x_c*y_c is the dot product of two vectors, ||x_c||||y_c|| is the product of the magnitude of two vectors, and the pearson correlation efficient equals: dot product of two vectors divided by the product of magnitude of two vectors.",
#     context="Explain the Pearson correlation coefficient (r) in terms of: a. What insights it can provide about data and how to interpret it."
# )

import psycopg
from utils.config import connection_dict
from utils.initiate_debate import initiate_debate
from models.prompt_models.query_model import QueryModel
from database_manager import add_debate

def process_all_responses():
    connection_string = " ".join(f"{key}={value}" for key, value in connection_dict.items())
    
    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:
            # Get all responses with their associated questions
            cur.execute("""
                SELECT 
                    r.id as response_id,
                    r.response_text,
                    q.id as question_id,
                    q.question_text,
                    q.question_title
                FROM responses r
                JOIN questions q ON r.question_id = q.id
            """)
            
            responses = cur.fetchall()
            
            for response in responses:
                response_id, response_text, question_id, question_text, question_title = response
                
                # Get all rubric components for this question
                cur.execute("""
                    SELECT id, component_text
                    FROM rubrics
                    WHERE question_id = %s
                """, (question_id,))
                
                rubrics = cur.fetchall()
                
                # Process each rubric component for this response
                for rubric_id, rubric_component in rubrics:
                    # Create query model for debate
                    query = QueryModel(
                        rubric_component=rubric_component,
                        student_response=response_text,
                        context=question_text
                    )
                    
                    try:
                        # Initiate debate
                        debate_result = initiate_debate(query)
                        
                        # Store debate result in database
                        add_debate(
                            conn=conn,
                            debate=debate_result,
                            rubric_id=rubric_id,
                            response_id=response_id
                        )
                        
                        print(f"Successfully processed response {response_id} with rubric {rubric_id}")
                        
                    except Exception as e:
                        print(f"Error processing response {response_id} with rubric {rubric_id}: {str(e)}")
                        continue

def main():
    try:
        process_all_responses()
        print("Successfully completed processing all responses")
    except Exception as e:
        print(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main()