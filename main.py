import tkinter as tk
from tkinter import ttk
from audio_stream import start_stream, stop_stream, terminate_pyaudio

# Create the GUI
app = tk.Tk()
app.title("Real-Time Anonymous Voice Processor")

# Start and stop stream buttons
start_button = ttk.Button(app, text="Start Stream", command=start_stream)
start_button.pack(pady=20)

stop_button = ttk.Button(app, text="Stop Stream", command=stop_stream)
stop_button.pack(pady=10)

# Close GUI properly
def on_closing():
    try:
        stop_stream()
        terminate_pyaudio()
        print("Closing application...")
    except Exception as e:
        print(f"Error closing stream: {e}")
    finally:
        app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
