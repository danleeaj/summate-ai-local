import psycopg
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
               INSERT INTO responses (question_id, response_text)
               VALUES (%s, %s)
               RETURNING id
               """,
               (response.question_id, response.response_text)
           )
           response_id = cur.fetchone()[0]
           
           conn.commit()
           return response_id
           
       except Exception as e:
           conn.rollback()
           raise e

def main():

    connection_string = " ".join(f"{key}={value}" for key, value in connection_dict.items())

    with psycopg.connect(connection_string) as conn:

        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS testing (
                    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    name character varying(255),
                    age integer,
                    gender character(1)
                );
            """)

            cur.execute("""INSERT INTO testing (name, age, gender)
                        VALUES ('Mike', 30, 'm')
                        RETURNING id;
                        """)
            response_id = cur.fetchone()[0]

            conn.commit()

            cur.close()
            conn.close()

            print(f"Inserted at {response_id}")

if __name__ == "__main__":
    main()