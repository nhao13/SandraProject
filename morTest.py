import wave
import numpy as np
import matplotlib.pyplot as plt

# Open the audio file
with wave.open('try.wav', 'r') as wav_file:
    # Get the number of audio frames in the file
    num_frames = wav_file.getnframes()
    # Read all audio frames as a byte string
    audio_bytes = wav_file.readframes(num_frames)

# Convert the byte string to a numpy array of integers
audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
print(audio_data.ndim)
# Define the length of the noise floor window
noise_window = int(wav_file.getframerate() * 2) # 2 seconds

# Calculate the mean amplitude of the first noise floor window
noise_floor = np.mean(np.abs(audio_data[:noise_window]))

# Set the initial threshold to the noise floor plus a safety margin
threshold = noise_floor * 1.5

# Detect the breaths above the threshold
diff = np.abs(np.diff(audio_data))
breaths = np.where(diff > threshold)[0]
print(len(breaths))
# Remove breaths that are too close together
min_distance = int(wav_file.getframerate() * 0.2) # 200 milliseconds
breaths = np.delete(breaths, np.where(np.diff(breaths) < min_distance)[0] + 1)
print(breaths)
# Count the number of breaths detected
num_breaths = len(breaths)/2

# Calculate the duration of the recording in seconds
duration = num_frames / wav_file.getframerate()

# Calculate the average breathing rate in breaths per second
avg_breathing_rate = num_breaths / duration

print("Number of breaths in the recording: ", num_breaths)
print("Duration of the recording: {:.2f} seconds".format(duration))
print("Average breathing rate: {:.2f} breaths per minute".format(avg_breathing_rate*60))

# Create a time array for the audio data
time = np.arange(0, len(audio_data)) / wav_file.getframerate()

# Plot the audio waveform and threshold
fig, ax = plt.subplots()
ax.plot(time, audio_data, label='Audio waveform')
ax.plot(time[:-1], diff, label='Audio difference')
ax.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
ax.set(xlabel='Time (s)', ylabel='Amplitude / Difference', title='Audio waveform and threshold')
ax.legend()
plt.show()