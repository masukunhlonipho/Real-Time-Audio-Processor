import pyaudio
from audio_processor import process_audio

# Parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = None

# Audio stream callback function
def audio_callback(in_data, frame_count, time_info, status):
    processed_data = process_audio(in_data, RATE, CHUNK)
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

# Proper cleanup
def terminate_pyaudio():
    global p
    p.terminate()
