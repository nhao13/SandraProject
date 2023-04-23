import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy
import math

# Open the audio file
with wave.open('Maor1.wav', 'r') as wav_file:
    # Get the number of audio frames in the file
    num_frames = wav_file.getnframes()
    # Read all audio frames as a byte string
    audio_bytes = wav_file.readframes(num_frames)

# Convert the byte string to a numpy array of integers
audio_data = np.frombuffer(audio_bytes, dtype=np.int16)


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


low_cut = 150
high_cut = 1200
samplerate = wav_file.getframerate()
y = butter_bandpass_filter(audio_data, low_cut, high_cut, samplerate)

# Define the length of the noise floor window
noise_window = int(samplerate * 2)  # 2 seconds

# Calculate the mean amplitude of the first noise floor window
noise_floor = np.mean(np.abs(y[:noise_window]))

# Set the initial threshold to the noise floor plus a safety margin
threshold = noise_floor

# Detect the breaths above the threshold
diff = np.abs(np.diff(y))
breaths = np.where(diff > threshold)[0]
# Remove breaths that are too close together
min_distance = int(samplerate * 0.2)  # 200 milliseconds
breaths = np.delete(breaths, np.where(np.diff(breaths) < min_distance)[0] + 1)
# Count the number of breaths detected
num_breaths = math.ceil(len(breaths)/2)

# Calculate the duration of the recording in seconds
duration = num_frames / wav_file.getframerate()

# Calculate the average breathing rate in breaths per second
avg_breathing_rate = num_breaths / duration

print("Number of breaths in the recording: ", num_breaths)
print("Duration of the recording: {:.2f} seconds".format(duration))
print("Average breathing rate: {:.2f} breaths per minute".format(avg_breathing_rate*60))

# Create a time array for the audio data
time = np.arange(0, len(y)) / wav_file.getframerate()

# Plot the audio waveform and threshold
fig, ax = plt.subplots()

breath_times = time[breaths]

ax.scatter(breath_times, np.zeros_like(breath_times), color='g', marker='o', label='Breath')
ax.plot(time[:-1], diff, label='Audio difference')
ax.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
ax.set(xlabel='Time (s)', ylabel='Amplitude / Difference', title='Audio waveform and threshold')
ax.legend()
plt.show()