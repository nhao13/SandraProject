import numpy as np
import scipy.signal as signal
from scipy.io import wavfile
import padasip as pa

# Load the audio file
samplerate, data = wavfile.read(r'C:\Users\UriMiron\Documents\Recordings\breathB.wav')

# Set filter parameters
lowcut = 80  # Hz
highcut = 2000  # Hz
order = 4
length = 0.1  # seconds
mu = 0.001  # step size for adaptive filter

# Create a Butterworth bandpass filter
b, a = signal.butter(order, [lowcut / (samplerate/2), highcut / (samplerate/2)], btype='band')

# Apply the filter to the audio data
filtered_data = signal.filtfilt(b, a, data[:, 0])

# Create an adaptive filter
nlms_filter = pa.filters.FilterNLMS(mu=mu, n=order+1)

# Use the sliding window technique to detect breaths
window_size = int(length * samplerate)
step_size = window_size // 2
breath_count = 0

for i in range(0, len(filtered_data) - window_size, step_size):
    window = filtered_data[i:i+window_size]
    
    # Apply the adaptive filter to the window
    x, e, w = nlms_filter.run(window, window)
    
    # Calculate the root mean square of the error signal
    rms = np.sqrt(np.mean(e**2))
    
    # If the RMS value is below a threshold, count it as a breath
    if rms < 0.01:
        breath_count += 1

print("Number of breaths detected:", breath_count)
