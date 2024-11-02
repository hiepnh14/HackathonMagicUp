import speech_recognition as sr
import tkinter as tk
import app
import pyaudio
import wave
import time
import openai
import numpy as np
# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize a list to store chat messages
chat_messages = []

# Function to update chat display
def update_chat_display():
    chat_display.delete("1.0", tk.END)  # Clear chat display
    # Show only the last 5 messages
    recent_messages = chat_messages[-5:]
    for message in recent_messages:
        chat_display.insert(tk.END, message + "\n")
    chat_display.see(tk.END)
def _record_audio():
    """Records audio and stops when there is no voice detected for 3 seconds."""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    SILENCE_THRESHOLD = 500  # Adjust based on microphone sensitivity
    MAX_SILENT_FRAMES = int(3 * RATE / CHUNK)  # 3 seconds of silence

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Check volume level
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.linalg.norm(audio_data)

        if volume < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0

        # Stop if silence is detected for 3 seconds
        if silent_chunks > MAX_SILENT_FRAMES:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save recorded frames to an audio buffer
    audio_data = io.BytesIO()
    wf = wave.open(audio_data, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    audio_data.seek(0)
    return audio_data

def _transcribe_audio(self, audio_data):
    """Sends audio data to Whisper API and returns the transcription."""
    response = openai.Audio.transcribe("whisper-1", audio_data)
    return response["text"]
# Function to record and transcribe speech
def record_speech():
    global chat_messages
    with sr.Microphone() as source:
        chat_messages.append("Listening...")
        print("Listening...")
        update_chat_display()
        try:
            # audio = recognizer.listen(source, phrase_time_limit=20, timeout=20)  # Adjust timeout if needed
            # text =  recognizer.recognize_google(audio)
            # audio = _record_audio()
            audio = recognizer.record(source, duration=5)
            # text = _transcribe_audio(audio)
            text =  recognizer.recognize_google(audio)
            # text = transcription.text
            user_message = "You: " + text
            chat_messages.append(user_message)
            print(text)
            app.main(text)
            # Simulate a computer response (can be customized)
            response = "Computer: I heard you say '" + text + "'"
            chat_messages.append(response)
            
            # Update chat display
            update_chat_display()
            
        except sr.UnknownValueError:
            chat_messages.append("Could not understand audio")
            update_chat_display()
        except sr.RequestError:
            chat_messages.append("Could not request results; check internet")
            update_chat_display()
        except Exception as e:
            chat_messages.append(f"Error: {e}")
            update_chat_display()

# Setup GUI
window = tk.Tk()
window.title("Speech to Text Chat Box")
window.geometry("400x300")

# Centered chat display (shows 5 most recent messages)
chat_display = tk.Text(window, width=50, height=10, wrap=tk.WORD, state=tk.NORMAL)
chat_display.pack(pady=20)

record_button = tk.Button(window, text="Record", command=record_speech)
record_button.pack()

window.mainloop()
