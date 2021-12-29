import gc
import os
import numpy
import glob
import subprocess
import re, string
import helper
import torch
import soundfile as sf
import time

from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


def idx_to_file(idx):
    return "/".join(idx.split("-")[:-1])

def wav2vec2_recognize_audio(audio_fpath):
    audio_input, _ = sf.read(audio_fpath)

    # transcribe
    input_values = tokenizer(audio_input, return_tensors="pt").input_values
    # input_values = input_values.to(self.device)

    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]

    del audio_input, input_values, logits, predicted_ids
    torch.cuda.empty_cache()
    gc.collect()

    print("Wav2Vec2 transcription: ", transcription)

    return transcription


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
    
    for root_dir in [
                    "LibriSpeech/test-clean/",
                     "LibriSpeech/dev-clean/",
                     "LibriSpeech/test-other/",
                     "LibriSpeech/dev-other/",
                     ]:

        # asr_name = "deepspeech"
        asr_name = "wav2vec2"
        
        if asr_name == "wav2vec2" :
            model_dir = "wav2vec2"
        elif asr_name == "deepspeech" :
            model_dir = "deepspeech"
            model_name = "deepspeech-0.9.3-models.pbmm"
            model_path = model_dir + "/" + model_name


        ## root_dir needs a trailing slash (i.e. /root/dir/)
        for filename in glob.iglob(root_dir + '**/*.trans.txt', recursive=True):
            
            # print(filename)
            # filename = "LibriSpeech/test-other/367/130732/367-130732.trans.txt"

            file = open(filename)

            for line in file.readlines() :
                idx = line.split()[0]
                text = " ".join(line.split()[1:])
                
                fname = os.path.join(root_dir, idx_to_file(idx), idx)
                flac_path = fname + ".flac"
                wav_path = fname + ".wav"
                transcription_path = fname + "." + model_dir + ".transcription.txt"

                # print("XXXX")
                # print("XXXX")
                # print("XXXX")
                # print(idx)
                # print(text)
                # print(transcription_path)

                    
                if not os.path.exists(wav_path):
                    convert_flac_to_wav(flac_path, wav_path)

                if (not os.path.exists(transcription_path)) or helper.is_empty_file(transcription_path):
                    
                    
                    if asr_name == "deepspeech" :
                        transcription = deepspeech_recognize_audio(model_path, wav_path)
                    elif asr_name == "wav2vec2" :
                        transcription = wav2vec2_recognize_audio(wav_path)

                    tfile = open(transcription_path, "w+")
                    tfile.write("%s\n" % transcription)
                    tfile.close()

            file.close()
