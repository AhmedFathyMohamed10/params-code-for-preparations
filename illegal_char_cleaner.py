import re

def clean_text(text):
    """
    Remove or replace illegal characters that cannot be used in Excel worksheets.
    """
    if text is None:
        return ''
    # Define illegal characters (you can add more if needed)
    illegal_chars = r'[\x00-\x1F\x7F-\x9F]'
    # Replace illegal characters with an empty string
    return re.sub(illegal_chars, '', text)
