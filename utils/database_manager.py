from pydantic import BaseModel
from pathlib import Path
import os
import sqlite3

# TODO: Store individual JSON files and their path for the debate
def storeJson(model_object: BaseModel, directory: str, filename) -> None:

    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / filename

    unpacked_json = model_object.model_dump_json()
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(unpacked_json)
        
    return file_path

# TODO: Store sqlite database
def create_database_directory():

    main_dir = Path(__file__).parent.parent.absolute()
    db_dir = os.path.join(main_dir, 'database')

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Created database directory at: {db_dir}")
    
    return db_dir

class DebateDatabase:
    def __init__(self, test_name: str):
        self.base_dir = create_database_directory()
        self.test_dir = Path(self.base_dir) / test_name
        self.test_dir.mkdir(exist_ok=True)

        self.debates_dir = self.test_dir / "debates"
        self.debates_dir.mkdir(exist_ok=True)
        
        self.db_path = self.test_dir / f"{test_name}.db"
        
        # Initialize database and create table
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS debates (
                response_id INTEGER,
                rubric_id INTEGER,
                evaluation INTEGER,
                evaluator TEXT,
                debate_id TEXT PRIMARY KEY
            )
        """)
        self.conn.commit()

    def add_row(self, row_data: tuple) -> str:
        """
        Adds a row to the database and returns the debate_id
        
        Args:
            row_data: tuple containing (response_id, rubric_id, evaluation, evaluator)
        
        Returns:
            debate_id: string in format "response_id_rubric_id_evaluator"
        """
        response_id, rubric_id, evaluation, evaluator, debate = row_data
        debate_id = f"{response_id}_{rubric_id}_{evaluator}"
        
        self.cursor.execute("""
            INSERT INTO debates 
            (response_id, rubric_id, evaluation, evaluator, debate_id)
            VALUES (?, ?, ?, ?, ?)
        """, (response_id, rubric_id, evaluation, evaluator, debate_id))
        
        self.conn.commit()

        storeJson(debate, self.debates_dir, debate_id)

        return debate_id

    def __del__(self):
        """Ensures database connection is closed when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()