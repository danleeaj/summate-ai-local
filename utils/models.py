from enum import Enum

class Model(Enum):
    """
    Represents the available LLM options for the debate system.
    """
    PHI = "phi3.5"
    GEMMA = "gemma2"
    LLAMA = "llama3.2"