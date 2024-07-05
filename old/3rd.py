import tkinter as tk
from tkinter import ttk
import pyaudio
import numpy as np
from scipy.signal import butter, lfilter, resample

# Parameters
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of audio channels
RATE = 44100  # Sample rate

# Pitch shifting factor (less than 1 to lower the pitch)
PITCH_FACTOR = 0.7

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = None

# Function to process audio (apply filter)
def process_audio(data, sample_rate):
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Resample to change the pitch
    resampled_data = resample(audio_data, int(len(audio_data) * PITCH_FACTOR))
    # Adjust the length back to original
    if len(resampled_data) < CHUNK:
        resampled_data = np.pad(resampled_data, (0, CHUNK - len(resampled_data)), mode='constant')
    else:
        resampled_data = resampled_data[:CHUNK]
    return resampled_data.astype(np.int16).tobytes()

# Audio stream callback function
def audio_callback(in_data, frame_count, time_info, status):
    processed_data = process_audio(in_data, RATE)
    return (processed_data, pyaudio.paContinue)

# Function to start the audio stream
def start_stream():
    global stream
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=audio_callback)
        print("Starting stream...")
        stream.start_stream()
    except Exception as e:
        print(f"Error starting stream: {e}")

# Function to stop the audio stream
def stop_stream():
    global stream
    try:
        if stream and stream.is_active():
            stream.stop_stream()
            stream.close()
            print("Stopping stream...")
    except Exception as e:
        print(f"Error stopping stream: {e}")
    finally:
        stream = None

# Create the GUI
app = tk.Tk()
app.title("Real-Time Audio Processor")

# Start and stop stream buttons
start_button = ttk.Button(app, text="Start Stream", command=start_stream)
start_button.pack(pady=20)

stop_button = ttk.Button(app, text="Stop Stream", command=stop_stream)
stop_button.pack(pady=10)

# Close GUI properly
def on_closing():
    try:
        if stream and stream.is_active():
            stream.stop_stream()
            stream.close()
        p.terminate()
        print("Closing application...")
    except Exception as e:
        print(f"Error closing stream: {e}")
    finally:
        app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
