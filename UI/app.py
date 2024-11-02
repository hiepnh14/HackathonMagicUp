import speech_recognition as sr
import tkinter as tk
import threading

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# Initialize recognizer
recognizer = sr.Recognizer()

class ChatApplication:
    def __init__(self):
        self.window = tk.Tk()
        self._setup_main_window()
    
    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Voice-Activated Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # Head label
        head_label = tk.Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # Tiny divider
        line = tk.Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # Text widget
        self.text_widget = tk.Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=tk.DISABLED)

        # Bottom label
        bottom_label = tk.Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # Message entry box
        self.msg_entry = tk.Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.58, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # Send button
        send_button = tk.Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.60, rely=0.008, relheight=0.06, relwidth=0.15)

        # Voice button
        voice_button = tk.Button(bottom_label, text="🎤 Voice", font=FONT_BOLD, width=20, bg=BG_GRAY, command=self._start_voice_thread)
        voice_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
    
    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, sender + ": " + msg + "\n")
        self.text_widget.configure(state=tk.DISABLED)
        
        if sender == "You":
            self.msg_entry.delete(0, tk.END)

        # Placeholder for bot response
        response = f"Bot: I received your message '{msg}'"
        self.text_widget.insert(tk.END, response + "\n")
        
        self.text_widget.see(tk.END)

    def _start_voice_thread(self):
        # Start the speech recognition in a separate thread to avoid freezing the GUI
        threading.Thread(target=self._voice_recognition, daemon=True).start()

    def _voice_recognition(self):
        with sr.Microphone() as source:
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.insert(tk.END, "Listening...\n")
            self.text_widget.configure(state=tk.DISABLED)
            self.text_widget.see(tk.END)
            
            try:
                audio = recognizer.listen(source, timeout=5)  # Listen for speech
                text = recognizer.recognize_google(audio)    # Recognize the speech
                self._insert_message(text, "You")
            except sr.UnknownValueError:
                self._insert_message("Could not understand audio", "System")
            except sr.RequestError:
                self._insert_message("Could not request results; check internet connection", "System")

if __name__ == "__main__":
    app = ChatApplication()
    app.run()

# Function to update chat display
# def update_chat_display():
#     chat_display.config(state=tk.NORMAL)
#     chat_display.delete("1.0", tk.END)  # Clear the display
#     # Show only last 5 messages
#     for message in chat_messages[-5:]:
#         chat_display.insert(tk.END, message + "\n")
#     chat_display.config(state=tk.DISABLED)
#     chat_display.see(tk.END)  # Scroll to the end

# # Function to record and transcribe speech
# def record_speech():
#     global chat_messages
#     while True:
#         chat_messages.append("Listening...")  # Display "Listening..."
#         update_chat_display()
        
#         with sr.Microphone() as source:
#             try:
#                 print("Recording...")
#                 audio = recognizer.listen(source)  # Adjust timeout if needed
#                 text = recognizer.recognize_google(audio)
#                 user_message = "You: " + text
#                 print(user_message)
#                 chat_messages.append(user_message)
                
#                 # Simulated computer response
#                 response = f"Computer: I heard you say '{text}'"
#                 chat_messages.append(response)
                
#             except sr.UnknownValueError:
#                 chat_messages.append("Could not understand audio")
#             except sr.RequestError:
#                 chat_messages.append("Could not request results; check internet")
#             except Exception as e:
#                 chat_messages.append(f"Error: {e}")
            
#             update_chat_display()  # Update the chat display
#             time.sleep(1)  # Add a brief pause between listens

# # Setup GUI
# window = tk.Tk()
# window.title("Always-Listening Speech Chatbox")
# window.geometry("400x300")

# chat_display = tk.Text(window, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
# chat_display.pack(pady=20)

# # Start continuous listening in a separate thread
# threading.Thread(target=record_speech, daemon=True).start()

# window.mainloop()
