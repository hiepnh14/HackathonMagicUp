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
def get_webcam_index():
    """Find and return the index of the webcam audio device."""
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        dev_info = pa.get_device_info_by_index(i)
        if "Webcam" in dev_info["name"]:
            print(f"Using device {i}: {dev_info['name']}")
            return i
    print("Webcam audio device not found.")
    return None
get_webcam_index = get_webcam_index()
# Function to record and transcribe speech
def record_speech(device=get_webcam_index):
    global chat_messages
    with sr.Microphone(device) as source:
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
