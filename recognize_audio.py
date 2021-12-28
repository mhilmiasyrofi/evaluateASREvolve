import os
import numpy
import glob
import subprocess
import re, string
import helper

def idx_to_file(idx):
    return "/".join(idx.split("-")[:-1])

def deepspeech_recognize_audio(model_path, audio_fpath):
    cmd = "deepspeech --model " + model_path + " --scorer deepspeech/deepspeech-0.9.3-models.scorer --audio " + audio_fpath

    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, _) = proc.communicate()

    transcription = out.decode("utf-8")[:-1]

    print("DeepSpeech transcription: %s" % transcription)
    return transcription

def convert_flac_to_wav(flac_path, wav_fpath):
    setting = " -acodec pcm_s16le -ac 1 -ar 16000 "
    cmd = f"ffmpeg -i {flac_path} {setting} {wav_fpath} -y"
    os.system(cmd)

if __name__ == "__main__" :

    root_dir = "LibriSpeech/dev-other/"
    
    model_dir = "deepspeech"
    model_name = "deepspeech-0.9.3-models.pbmm"
    
    # model_dir = "finetuned_deepspeech"
    # model_name = "output_graph.pbmm"

    model_path = model_dir + "/" + model_name

    ### root_dir needs a trailing slash (i.e. /root/dir/)
    for filename in glob.iglob(root_dir + '**/*.trans.txt', recursive=True):
        
        # print(filename)
        # filename = "LibriSpeech/test-clean/61/70968/61-70968.trans.txt"

        file = open(filename)

        for line in file.readlines() :
            idx = line.split()[0]
            text = " ".join(line.split()[1:])
            
            fname = os.path.join(root_dir, idx_to_file(idx), idx)
            flac_path = fname + ".flac"
            wav_path = fname + ".wav"
            transcription_path = fname + "." + model_dir + ".transcription.txt"

            if not os.path.exists(wav_path):
                convert_flac_to_wav(flac_path, wav_path)

            if (not os.path.exists(transcription_path)) or helper.is_empty_file(transcription_path):
                transcription = deepspeech_recognize_audio(model_path, wav_path)

                tfile = open(transcription_path, "w+")
                tfile.write("%s\n" % transcription)
                tfile.close()

        file.close()
