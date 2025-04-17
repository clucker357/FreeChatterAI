# package import
import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


def audio_trim(file_name):
    wav, sr = librosa.load(file_name, sr=None)
    yt, index = librosa.effects.trim(wav, top_db=20)
    sf.write("trimmed_input.wav", yt, sr)
    output_file = "trimmed_input.wav"
    return output_file