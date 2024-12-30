from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLineEdit, QTextEdit, QPushButton, 
                              QLabel, QComboBox, QScrollArea, QTabWidget, QSpinBox,
                              QPlainTextEdit)

import sys
import psycopg

from utils.config import connection_dict

from models.database_models.question_model import QuestionModel
from models.database_models.rubric_model import RubricModel
from models.database_models.response_model import ResponseModel

from database_manager import add_question, add_response

class RubricComponentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        
        # Score input
        self.score_label = QLabel("Score:")
        self.score_input = QSpinBox()
        self.score_input.setMinimum(0)
        self.score_input.setMaximumWidth(60)
        
        # Text input
        self.text_input = QPlainTextEdit()
        self.text_input.setMaximumHeight(50)
        
        # Remove button
        self.remove_button = QPushButton("-")
        self.remove_button.setMaximumWidth(30)
        
        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.score_input)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.remove_button)
        
        self.remove_button.clicked.connect(self.remove_self)
        
    def remove_self(self):
        self.setParent(None)
        self.deleteLater()
        
    def get_data(self):
        return {
            'score': self.score_input.value() or None,
            'component_text': self.text_input.toPlainText()
        }

class AddQuestionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Question title
        title_layout = QHBoxLayout()
        self.title_label = QLabel("Question Title (optional):")
        self.title_input = QLineEdit()
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.title_input)
        
        # Question content
        content_layout = QVBoxLayout()
        self.content_label = QLabel("Question Content:")
        self.content_input = QTextEdit()
        content_layout.addWidget(self.content_label)
        content_layout.addWidget(self.content_input)
        
        # Rubric components
        self.rubric_label = QLabel("Rubric Components:")
        self.rubric_container = QWidget()
        self.rubric_layout = QVBoxLayout(self.rubric_container)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.rubric_container)
        self.scroll_area.setWidgetResizable(True)
        
        self.add_rubric_button = QPushButton("Add Rubric Component")
        self.add_rubric_button.clicked.connect(self.add_rubric_component)
        
        self.submit_button = QPushButton("Submit Question")
        self.submit_button.clicked.connect(self.submit_question)
        
        # Add everything to main layout
        self.layout.addLayout(title_layout)
        self.layout.addLayout(content_layout)
        self.layout.addWidget(self.rubric_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.add_rubric_button)
        self.layout.addWidget(self.submit_button)
        
        # Add initial rubric component
        self.add_rubric_component()
        
    def add_rubric_component(self):
        component = RubricComponentWidget()
        self.rubric_layout.addWidget(component)
        
    def submit_question(self):
        title = self.title_input.text()
        content = self.content_input.toPlainText()
        
        if not content:
            return  # Add error handling here
            
        # Collect rubric components
        rubric_components = []
        for i in range(self.rubric_layout.count()):
            widget = self.rubric_layout.itemAt(i).widget()
            if isinstance(widget, RubricComponentWidget):
                data = widget.get_data()
                if data['component_text']:  # Only add if there's text
                    rubric_components.append(RubricModel(**data))
                    
        # Create question model
        question = QuestionModel(
            question_title=title if title else None,
            question_text=content
        )
        
        # Submit to database
        connection_string = " ".join(f"{key}={value}" for key, value in connection_dict.items())
        with psycopg.connect(connection_string) as conn:
            add_question(conn, question, rubric_components)
        
        sys.exit(app.exec())
            
        # Clear inputs
        # self.title_input.clear()
        # self.content_input.clear()
        # while self.rubric_layout.count():
        #     widget = self.rubric_layout.itemAt(0).widget()
        #     if widget:
        #         widget.deleteLater()
        # self.add_rubric_component()

class AddResponseWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Question selector
        self.question_label = QLabel("Select Question:")
        self.question_combo = QComboBox()
        self.refresh_questions()

        # Identifier
        self.id_label = QLabel("Identifier:")
        self.id_input = QLineEdit()
        
        # Response text
        self.response_label = QLabel("Response Text:")
        self.response_input = QTextEdit()
        
        self.submit_button = QPushButton("Submit Response")
        self.submit_button.clicked.connect(self.submit_response)
        
        # Add to layout
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.question_combo)
        self.layout.addWidget(self.id_label)
        self.layout.addWidget(self.id_input)
        self.layout.addWidget(self.response_label)
        self.layout.addWidget(self.response_input)
        self.layout.addWidget(self.submit_button)
        
    def refresh_questions(self):
        self.question_combo.clear()
        connection_string = " ".join(f"{key}={value}" for key, value in connection_dict.items())
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, question_title, question_text FROM questions")
                questions = cur.fetchall()
                for q_id, title, text in questions:
                    display_text = title if title else text[:50] + "..."
                    self.question_combo.addItem(display_text, q_id)
                    
    def submit_response(self):
        question_id = self.question_combo.currentData()
        response_text = self.response_input.toPlainText()
        identifier = self.id_input.text()
        
        if not response_text:
            return  # Add error handling
            
        response = ResponseModel(
            identifier=identifier,
            question_id=question_id,
            response_text=response_text
        )
        
        connection_string = " ".join(f"{key}={value}" for key, value in connection_dict.items())
        with psycopg.connect(connection_string) as conn:
            add_response(conn, response)
            
        # Clear input
        self.response_input.clear()
        self.id_input.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Question and Response Manager")
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Add question tab
        self.question_widget = AddQuestionWidget()
        self.tabs.addTab(self.question_widget, "Add Question")
        
        # Add response tab
        self.response_widget = AddResponseWidget()
        self.tabs.addTab(self.response_widget, "Add Response")
        
        self.resize(800, 600)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {e}")