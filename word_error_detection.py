import os
import numpy, pandas

from asr_evaluation.asr_evaluation import asr_evaluation

from diff_match_patch import python3 as dmp_module

if __name__ == "__main__":
    
    reference       = "show this help message and exit"
    transcription   = "show thi help message and then exi"

    # reference       = "how this help message and exit"
    # transcription   = "show thi help message and then exi"

    
    ## https://github.com/mhilmiasyrofi/asr-evaluation
    evaluation = asr_evaluation.ASREvaluation()
    evaluation.detect_word_error(reference, transcription)
    confusion = evaluation.get_confusions()
    print(confusion)
    # asr_evaluation.print_confusions()



    print("Reference: \t", reference)
    print("Transcription: \t", transcription)

    ## https://github.com/google/diff-match-patch
    dmp = dmp_module.diff_match_patch()
    diff = dmp.diff_main(reference, transcription)
    # Result: [(-1, "Hell"), (1, "G"), (0, "o"), (1, "odbye"), (0, " World.")]
    dmp.diff_cleanupSemantic(diff)
    # Result: [(-1, "Hello"), (1, "Goodbye"), (0, " World.")]
    print(diff)

    (text1, text2, linearray) = dmp.diff_linesToChars(reference, transcription)
    # print(a)
    
    diffs = dmp.diff_main(reference, transcription, False)
    # print(diffs)
    # dmp.diff_charsToLines(diffs, lineArray)
        
    
