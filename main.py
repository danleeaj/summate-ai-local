import psycopg
from utils.config import connection_dict
from utils.initiate_debate import initiate_debate
from models.prompt_models.query_model import QueryModel
from database_manager import add_debate

from datetime import datetime

def process_unevaluated_responses():
    connection_string = " ".join(f"{key}={value}" for key, value in connection_dict.items())
    
    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT 
                    r.id as response_id,
                    r.response_text,
                    q.id as question_id,
                    q.question_text,
                    q.question_title,
                    ru.id as rubric_id,
                    ru.component_text
                FROM responses r
                JOIN questions q ON r.question_id = q.id
                JOIN rubrics ru ON q.id = ru.question_id
                LEFT JOIN debates1 d ON r.id = d.response_id AND ru.id = d.rubric_id
                WHERE d.id IS NULL
            """)
            
            unevaluated = cur.fetchall()
            
            for record in unevaluated:
                response_id, response_text, question_id, question_text, question_title, rubric_id, rubric_component = record
                
                query = QueryModel(
                    rubric_component=rubric_component,
                    student_response=response_text,
                    context=question_text
                )
                
                try:

                    debate_result = initiate_debate(query)
                    
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
    
    start_time = datetime.now()
    print(f"Starting processing at: {start_time}")
    
    try:
        process_unevaluated_responses()
        print("Successfully completed processing unevaluated responses")
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
    finally:
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"Finished at: {end_time}")
        print(f"Total processing time: {duration}")
    

if __name__ == "__main__":
    main()