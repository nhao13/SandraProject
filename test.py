import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
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

samplerate, data = wavfile.read(r"C:\Users\UriMiron\Documents\Recordings\breath.wav")
length = data.shape[0] / samplerate
time = np.linspace(0., length, data.shape[0])




lowcut= 500
highcut= 1500

y = butter_bandpass_filter(data, lowcut, highcut, samplerate, order=6)
plt.plot(time, y[:, 1], label='Filtered signal')
plt.xlabel('time (seconds)')
plt.grid(True)
plt.axis('tight')
plt.legend(loc='upper left')
plt.show()


peaks, _=   scipy.signal.find_peaks(y[:, 1],distance=5000, height=0.01, width=1250)

print(peaks)