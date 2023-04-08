import numpy as np
import matplotlib.pyplot as plt
import wave
import scipy.io
import padasip as pa
import math

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = scipy.signal.butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = scipy.signal.lfilter(b, a, data)
    return y

with wave.open('try.wav', 'r') as wav_file:
    # Get the number of audio frames in the file
    num_frames = wav_file.getnframes()
    # Read all audio frames as a byte string
    audio_bytes = wav_file.readframes(num_frames)

# Convert the byte string to a numpy array of integers
audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
samplerate= wav_file.getframerate()
time= np.arange(0, len(audio_data)) / samplerate




lowcut= 500
highcut= 1500
y = butter_bandpass_filter(audio_data, lowcut, highcut, samplerate)
plt.plot(time, y, label='Filtered signal')
plt.xlabel('time (seconds)')
plt.grid(True)
plt.axis('tight')
plt.legend(loc='upper left')
plt.show()
width=samplerate*0.3
print(audio_data.ndim)
peaks= scipy.signal.find_peaks_cwt(audio_data, width)
print(len(peaks))