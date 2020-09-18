from scipy.io import wavfile
import webrtcvad
import struct
from scipy.io.wavfile import write
import os
import numpy as np

# %matplotlib inline
import matplotlib.pyplot as plt
filename="G:\python\ws\study\study_pyqudio\\record20200807152733.wav"
sample_rate, samples = wavfile.read(filename)
vad = webrtcvad.Vad()
vad.set_mode(3)

raw_samples = struct.pack("%dh" % len(samples), *samples)

window_duration = 0.03
samples_per_window = int(window_duration * sample_rate + 0.4)
bytes_per_sample = 2