import pandas as pd
import numpy as np
import jiwer
import re
import string
from normalise import normalise, tokenize_basic

def read_transcription(fpath:str)->str:
    file = open(fpath)
    transcription = file.readline()
    file.close()

    return transcription


def remove_hex(text:str)->str:
    """
    Example: 
    "\xe3\x80\x90Hello \xe3\x80\x91 World!"
    """
    res = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i+1 < len(text) and text[i+1] == "x":
            i += 3
            res.append(" ")
        else:
            res.append(text[i])
        i += 1
    return "".join(res)


def remove_punctuation(text:str)->str:
    return text.translate(str.maketrans('', '', string.punctuation))


def remove_multiple_whitespace(text:str)->str:
    """
    remove multiple whitespace
    it covers tabs and newlines also
    """
    return re.sub(' +', ' ', text.replace('\n', ' ').replace('\t', ' ')).strip()


def normalize_text(text:str)->str:
    return " ".join(normalise(text, tokenizer=tokenize_basic, verbose=False))


## TODO check missus and mister again
def substitute_word(text:str)->str:
    """
    word subsitution to make it consistent
    """
    words = text.split(" ")
    preprocessed = []
    for w in words:
        substitution = ""
        if w == "mister":
            substitution = "mr"
        elif w == "missus":
            substitution = "mrs"
        else:
            substitution = w
        preprocessed.append(substitution)
    return " ".join(preprocessed)


def preprocess_text(text: str) -> str:
    text = text.lower()
    text = remove_hex(text)
    text = remove_punctuation(text)
    
    ## it takes long time to normalize
    ## skip this first
    try:
        text = normalize_text(text)
    except:
        text = text
    
    text = remove_punctuation(text)
    text = substitute_word(text)
    text = jiwer.RemoveMultipleSpaces()(text)
    text = jiwer.ExpandCommonEnglishContractions()(text)
    text = jiwer.RemoveWhiteSpace(replace_by_space=True)(
        text)  # must remove trailing space after it
    text = jiwer.Strip()(text)
    return text


def is_empty_file(fpath: str) -> bool:
    file = open(fpath)
    line = file.readline()
    line = line
    file.close()
    if line == "":
        return True
    return False


if __name__ == "__main__" :
    text = ""
    preprocess_text(text)

    
