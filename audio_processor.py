import numpy as np
from scipy.signal import butter, lfilter, resample

# Transformation parameters
PITCH_FACTOR = 0.7
MODULATION_RATE = 5
NOISE_LEVEL = 0.02

def process_audio(data, sample_rate, chunk):
    audio_data = np.frombuffer(data, dtype=np.int16)
    
    # Resample to change the pitch
    resampled_data = resample(audio_data, int(len(audio_data) * PITCH_FACTOR))
    
    # Adjust the length back to original
    if len(resampled_data) < chunk:
        resampled_data = np.pad(resampled_data, (0, chunk - len(resampled_data)), mode='constant')
    else:
        resampled_data = resampled_data[:chunk]
    
    # Apply modulation (tremolo effect)
    t = np.linspace(0, chunk / sample_rate, chunk, endpoint=False)
    modulation = 0.5 * (1.0 + np.sin(2.0 * np.pi * MODULATION_RATE * t))
    modulated_data = resampled_data * modulation
    
    # Add noise
    noise = NOISE_LEVEL * np.random.randn(chunk)
    noisy_data = modulated_data + noise
    
    # Apply low-pass filter
    b, a = butter(2, 1000 / (0.5 * sample_rate), btype='low')
    filtered_data = lfilter(b, a, noisy_data)
    
    return filtered_data.astype(np.int16).tobytes()
