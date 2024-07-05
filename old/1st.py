import pyaudio
import numpy as np
from scipy.signal import butter, lfilter

# Parameters
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of audio channels
RATE = 44100  # Sample rate

def process_audio(data, sample_rate):
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Simple low-pass filter for demonstration (more complex effects can be added)
    b, a = butter(2, 1000 / (0.5 * sample_rate), btype='low')
    filtered_data = lfilter(b, a, audio_data)
    return filtered_data.astype(np.int16).tobytes()

def callback(in_data, frame_count, time_info, status):
    processed_data = process_audio(in_data, RATE)
    return (processed_data, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)

print("Starting stream...")
stream.start_stream()

# Keep the stream running
try:
    while stream.is_active():
        pass
except KeyboardInterrupt:
    pass

print("Stopping stream...")
stream.stop_stream()
stream.close()
p.terminate()
