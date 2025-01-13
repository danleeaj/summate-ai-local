from utils.database_manager import DebateDatabase
from pydantic import BaseModel

class TestModel(BaseModel):
    test: bool
    

# Initialize database
db = DebateDatabase("test_run_1")

# Add a row
row_data = (1, 2, 1, "evaluator_1", TestModel(test=True))  # response_id, rubric_id, evaluation, evaluator
debate_id = db.add_row(row_data)
print(debate_id)  # Will print: "1_2_evaluator_1"