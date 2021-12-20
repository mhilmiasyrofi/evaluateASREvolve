import pandas as pd
import numpy as np
import jiwer

def min_edit_distance(word1:str, word2:str) -> int:
    """Calculate minimum edit distance from two words

    Args:
        word1: the first word
        word2: the second word
    
    Returns:
        The minimum edit character
    """

    m = len(word1)
    n = len(word2)

    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])      # Replace

    return dp[m][n]


def error_word_detection(ground_truth: str, transcription:str):
    errors = {}
    tokens1 = ground_truth.split()
    tokens2 = transcription.split()

    i = 0
    j = 0

    while i < len(tokens1) and j < len(tokens2):



    return errors

def preprocess_text(text: str) -> str :

    text = jiwer.RemoveMultipleSpaces()(text)
    text = jiwer.Strip()(text)
    text = jiwer.ReduceToListOfListOfWords()(text)
    
    return text

def test_min_edit_distance():
    print(min_edit_distance("ab", "ab"))
    print(min_edit_distance("ab", "abc"))
    print(min_edit_distance("bc", "abc"))
    print(min_edit_distance("cab", "abc"))


def test_error_word_detection():
    ground_truth = "he began a confused complain against the wizard"
    transcription = "he begin a confused complaint again the wizard"

    ground_truth = preprocess_text(ground_truth)
    transcription = preprocess_text(transcription)
    errors = error_word_detection(ground_truth, transcription)
    print(errors)


if __name__ == "__main__" :


    # test_min_edit_distance() # test min edit distance function

    test_error_word_detection() # test error detection function

