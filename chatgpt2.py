import scipy.io.wavfile as wavfile
import numpy as np

# Define parameters
filename = 'breathing.wav'
window_size = 1024
hop_size = 256
threshold = 0.05

# Load audio file
sample_rate, audio_data = wavfile.read(r'C:\Users\UriMiron\Documents\Recordings\breathB.wav')

# Calculate spectrogram
spec_data, _, _ = np.histogram2d(
    np.arange(audio_data.size),
    np.abs(np.fft.fft(audio_data))[:(audio_data.size // 2)],
    bins=[audio_data.size, window_size // 2],
    range=[[0, audio_data.size], [0, sample_rate // 2]]
)

# Apply median filter to spectrogram
spec_data = scipy.signal.medfilt(spec_data, kernel_size=[3, 3])

# Find peaks in spectrogram
peaks, _ = scipy.signal.find_peaks(spec_data, height=threshold*np.max(spec_data))

# Convert peak indices to time values
times = (peaks * hop_size) / sample_rate

# Print times of detected breaths
print(times)