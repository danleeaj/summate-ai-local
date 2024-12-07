from query_model import query_model
from utils.models import Model

print(query_model("Respond to this message with 'hi'. Structure your response as a json. Do not add any explanations.", Model.GEMMA))