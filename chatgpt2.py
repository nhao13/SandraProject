import numpy as np
import scipy.signal as sig
import soundfile as sf
import matplotlib.pyplot as plt

# Load audio file
filename = "breathB.wav"
data, sample_rate = sf.read(filename)

# Define bandpass filter
lowcut = 50
highcut = 1000
order = 4
b, a = sig.butter(order, [lowcut/(sample_rate/2), highcut/(sample_rate/2)], btype='band')
# Apply filter to audio data
filtered_data = sig.filtfilt(b, a, data)

# Find peaks in the filtered data
peaks, _ = sig.find_peaks(filtered_data, distance=100, height=0.1)

# Plot the original and filtered audio signals with detected peaks
plt.figure(figsize=(10, 8))
plt.subplot(211)
plt.plot(data)
plt.title('Original Recording')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.subplot(212)
plt.plot(filtered_data)
plt.plot(peaks, filtered_data[peaks], "x")
plt.title('Filtered Recording with Detected Peaks')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.show()