from enum import Enum

class LLMModel(Enum):
    """
    Represents the available LLM options for the debate system.
    """
    PHI = "phi3.5"
    GEMMA = "gemma2"
    LLAMA = "llama3.2"
    GEMMA_2B = "gemma2:2b"
    QWEN2 = "qwen2"