# Function to load Tacotron 2 model
def load_tacotron2_model():
    global tacotron2
    try:
        # Load Tacotron 2 model with CPU mapping
        tacotron2 = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_tacotron2', pretrained=True, map_location=torch.device('cpu'))
        tacotron2.eval()
        print("Tacotron 2 model loaded successfully.")
    except Exception as e:
        print(f"Error loading Tacotron 2 model: {e}")

# Function to load WaveGlow model
def load_waveglow_model():
    global waveglow
    try:
        # Load WaveGlow model with CPU mapping
        waveglow = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_waveglow', pretrained=True, map_location=torch.device('cpu'))
        waveglow = waveglow.remove_weightnorm(waveglow)
        waveglow.eval()
        print("WaveGlow model loaded successfully.")
    except Exception as e:
        print(f"Error loading WaveGlow model: {e}")

print(f"torch.cuda.is_available(): {torch.cuda.is_available()}")

# Load Tacotron 2 and WaveGlow models
print("Loading Tacotron 2 model...")
load_tacotron2_model()
print("Loading WaveGlow model...")
load_waveglow_model()
