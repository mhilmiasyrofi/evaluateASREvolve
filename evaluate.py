import os
import numpy
import glob
import jiwer


def idx_to_file(idx):
    return "/".join(idx.split("-")[:-1])

def read_transcription(fpath):
    file = open(fpath)
    transcription = file.readline()
    file.close()

    return transcription

if __name__ == "__main__":

    root_dir = "LibriSpeech/test-clean/"

    model_dir = "deepspeech"
    # model_dir = "finetuned_deepspeech"

    wers = []

    ### root_dir needs a trailing slash (i.e. /root/dir/)
    for filename in glob.iglob(root_dir + '**/*.trans.txt', recursive=True):
        # print(filename)

        # filename = "LibriSpeech/test-clean/61/70968/61-70968.trans.txt"

        
        file = open(filename)

        for line in file.readlines():
        # for line in file.readlines()[0:1]:
            idx = line.split()[0]
            text = " ".join(line.split()[1:])

            fname = os.path.join(root_dir, idx_to_file(idx), idx)
            flac_path = fname + ".flac"
            wav_path = fname + ".wav"
            transcription_path = fname + "." + model_dir + ".transcription.txt"

            if os.path.exists(transcription_path):
                transcription = read_transcription(transcription_path)

                transcription = transcription.lower()
                text = text.lower()
                
                wer = jiwer.wer(text, transcription)
                wers.append(wer)
                # print()
                # print()
                # print("text: ", text)
                # print("transcription: ",  transcription)
                # print("wer: ", wer)
            else :
                # continue
                raise ValueError("missing transcription: " + transcription_path)
            
        file.close()

    print(f"Average WER: {100 * sum(wers) / len(wers):.2f}%")
