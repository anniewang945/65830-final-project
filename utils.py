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

# assumes that a unqiue row will only appear once
def compare_accuracy(test, target):
    # apparently this is what lab 2 does regardless of orderby (makes a set and checks against the set which is much more complicate in golang)
    # it returns a boolean, but here we want to return accuracy
    incorrect = len(set(target).symmetric_difference(set(test)))
    overall = len(target)
    return "Accuracy of test results (length {}) vs target results (length {}) is {}".format(len(test), len(target), (overall-incorrect)/overall)