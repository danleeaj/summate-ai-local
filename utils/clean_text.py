import string

def clean_text_for_db(text: str) -> str:
    """
    Removes all punctuation from text while preserving spaces and basic structure.
    Returns cleaned text safe for database storage.
    
    Args:
        text (str): Input text to be cleaned
        
    Returns:
        str: Cleaned text with punctuation removed
    """
    if text:
        punctuation_to_remove = ''.join(char for char in string.punctuation if char not in '.,!?')
        translator = str.maketrans('', '', punctuation_to_remove)
        cleaned_text = text.translate(translator)
        cleaned_text = ' '.join(cleaned_text.split())
    else:
        return ""
    
    return cleaned_text

if __name__ == "__main__":
    text = """Hello, world! This is text 'with' potentially \\\\\\    
    issue causing stuff."""
    cleaned = clean_text_for_db(None)
    print(cleaned)