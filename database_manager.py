from utils.config import connection_dict
from typing import List

from models.debate_models.debate_model import DebateModel

from models.database_models.question_model import QuestionModel
from models.database_models.response_model import ResponseModel
from models.database_models.rubric_model import RubricModel

def add_debate(conn, debate: DebateModel, rubric_id: int, response_id: int) -> str:

    with conn.cursor() as cur:

        try:

            cur.execute(
                """
                INSERT INTO debates (evaluation, debate, rubric_id, response_id) 
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    debate.evaluation == "Yes",
                    debate.model_dump_json(),
                    rubric_id,
                    response_id,
                )
            )
            debate_id = cur.fetchone()[0]

            conn.commit()
            return debate_id
        
        except Exception as e:
            conn.rollback()
            raise e

def add_question(conn, question: QuestionModel, rubric_components: List[RubricModel]) -> int:

    if not question.question_title:
        question.question_title = question.question_text[:20]

    with conn.cursor() as cur:

        try:

            cur.execute(
                """
                INSERT INTO questions (question_title, question_text)
                VALUES (%s, %s)
                RETURNING id
                """,
                (question.question_title, question.question_text)
            )
            question_id = cur.fetchone()[0]
            
            for rubric in rubric_components:
                cur.execute(
                    """
                    INSERT INTO rubrics (question_id, component_text)
                    VALUES (%s, %s)
                    """,
                    (question_id, rubric.component_text)
                )
            
            conn.commit()
            return question_id
            
        except Exception as e:
            conn.rollback()
            raise e

def add_response(conn, response: ResponseModel) -> int:

   with conn.cursor() as cur:
       try:

           cur.execute(
               """
               INSERT INTO responses (question_id, response_text, unique_id)
               VALUES (%s, %s, %s)
               RETURNING id
               """,
               (response.question_id, response.response_text, response.identifier)
           )
           response_id = cur.fetchone()[0]
           
           conn.commit()
           return response_id
           
       except Exception as e:
           conn.rollback()
           raise e

def main():

    # connection_string = " ".join(f"{key}={value}" for key, value in connection_dict.items())

    # question = QuestionModel(question_title="Pearson coefficient", question_text="Explain the Pearson correlation coefficient (r) in terms of: a. What insights it can provide about data and how to interpret it. b. How it can be calculated (step-by-step) using the dot product of two vectors. c. EXTRA CREDIT: Using vectors [3, 9] and [1, 3], calculate the Pearson correlation coefficient.")

    # rubric_components = [
    #     RubricModel(score=1,component_text="Response states that the Pearson correlation coefficient measures the strength of a linear relationship"),
    #     RubricModel(score=1,component_text="Response explains that +1 indicates a perfect positive linear relationship"),
    #     RubricModel(score=1,component_text="Response explains that the coefficient ranges from -1 to +1"),
    #     RubricModel(score=1,component_text="Response explains that -1 indicates a perfect negative linear relationship"),
    #     RubricModel(score=1,component_text="Response explains that values closer to 0 indicate weaker relationships"),
    # ]

    # with psycopg.connect(connection_string) as conn:

    #     add_question(conn, question, rubric_components)

    return

if __name__ == "__main__":
    main()