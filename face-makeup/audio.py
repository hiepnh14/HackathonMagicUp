import pyttsx3
import speech_recognition as sr
import pyaudio
import os

os.system("pactl set-default-sink bluez_sink.F4_4E_FD_67_01_03.a2dp_sink")
# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

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

def get_audio(device_index):
    r = sr.Recognizer()
    with sr.Microphone(device_index=device_index) as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source)  # Adjust for background noise
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            said = r.recognize_google(audio)
            print("You said:", said)
            return said.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
        except Exception as e:
            print("Exception:", str(e))
        return ""

WAKE = "hi"
BYE = "bye"

# Get the WebCam device index
webcam_index = get_webcam_index()
def record_speech(device=get_webcam_index()):
    global chat_messages
    recognizer = sr.Recognizer()
    with sr.Microphone(device) as source:
        
        print("Listening...")
        
        try:
            # audio = recognizer.listen(source, phrase_time_limit=20, timeout=20)  # Adjust timeout if needed
            # text =  recognizer.recognize_google(audio)
            # audio = _record_audio()
            audio = recognizer.record(source, duration=5)
            # text = _transcribe_audio(audio)
            text =  recognizer.recognize_google(audio)
            # text = transcription.text
            
            print(text)
            
            # Simulate a computer response (can be customized)
            return text
            
        except sr.UnknownValueError:
            print("Could not understand audio")
            
        except sr.RequestError:
            print("Could not request results; check internet")
            
        except Exception as e:
            print(f"Error: {e}")

