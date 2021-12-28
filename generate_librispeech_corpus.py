import os
import numpy
import glob
import subprocess
import helper

def idx_to_file(idx):
    return "/".join(idx.split("-")[:-1])

if __name__ == "__main__":

    mode = "test-other"
    
    root_dir = f"LibriSpeech/{mode}/"

    corpus_fpath = f"LibriSpeech/{mode}-corpus.txt"

    with open(corpus_fpath, 'w') as corpus_file:

        ### root_dir needs a trailing slash (i.e. /root/dir/)
        for filename in glob.iglob(root_dir + '**/*.trans.txt', recursive=True):
            
            file = open(filename)
            for line in file.readlines():
                idx = line.split()[0]
                text = " ".join(line.split()[1:])

                text = helper.preprocess_text(text)

                corpus_file.write(text + "\n")

            file.close()

