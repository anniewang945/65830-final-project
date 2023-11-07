import tiktoken
from sentence_transformers import util

DEFAULT_ENC = "cl100k_base"

def num_tokens_from_string(string: str, encoding=DEFAULT_ENC) -> int:
    """
    Returns the number of tokens in a text string.
    """
    encoding = tiktoken.get_encoding(encoding)
    num_tokens = len(encoding.encode(string))
    return num_tokens