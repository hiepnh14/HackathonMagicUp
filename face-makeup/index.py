import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from audio import get_audio, speak, get_webcam_index, record_speech
from mainUI import MagicUpApp
import threading

gif_path = "pic/face-makeup.gif"
mic_gif_path = "pic/microphone-recording.gif"

WAKE = "hi"
BYE = "bye"
full_text = "ARE YOU READY TO BE BEAUTIFUL?"

flash_count = 0

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MAGICUP")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.quit())
        
        self.listener_active = True
        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(expand=True)
        
        self.text_label = tk.Label(self.frame, font=("Arial", 30), fg="white", bg="black", anchor="w", justify="left")
        self.text_label.pack(fill="x", padx=20)

        self.webcam_index = get_webcam_index()
        if self.webcam_index is None:
            print("No valid webcam audio device found. Exiting.")
            self.root.quit()

        self.setup_gif_animation()
        self.display_text()
        self.setup_microphone_icon()

        self.prompt_label = tk.Label(self.mic_frame, text="Try to say: 'Hi' to start! And tell me what makeup do you want!", 
                                     font=("Arial", 20), fg="white", bg="black")
        self.prompt_label.pack(side="left")

        self.start_listening()

    def setup_gif_animation(self):
        gif_image = Image.open(gif_path)
        new_size = (int(gif_image.width * 0.7), int(gif_image.height * 0.7))
        self.frames = [ImageTk.PhotoImage(frame.copy().resize(new_size, Image.LANCZOS)) for frame in ImageSequence.Iterator(gif_image)]
        self.frame_index = 0
        self.gif_label = tk.Label(self.frame, bg="black")
        self.gif_label.pack(pady=20)
        self.update_gif()

    def update_gif(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.gif_label.config(image=self.frames[self.frame_index])
        self.root.after(int(100), self.update_gif)

    def setup_microphone_icon(self):
        mic_image = Image.open(mic_gif_path)
        mic_new_size = (int(mic_image.width * 0.1), int(mic_image.height * 0.1))
        self.mic_frames = [ImageTk.PhotoImage(frame.copy().resize(mic_new_size, Image.LANCZOS)) for frame in ImageSequence.Iterator(mic_image)]
        self.mic_frame_index = 0

        self.mic_frame = tk.Frame(self.root, bg="black")
        self.mic_frame.pack(side="bottom", pady=10)
        self.mic_label = tk.Label(self.mic_frame, bg="black")
        self.mic_label.pack(side="left", padx=(0, 10))
        self.update_mic_gif()

    def update_mic_gif(self):
        self.mic_frame_index = (self.mic_frame_index + 1) % len(self.mic_frames)
        self.mic_label.config(image=self.mic_frames[self.mic_frame_index])
        self.root.after(int(100), self.update_mic_gif)

    def start_listening(self):
        if self.webcam_index is not None:
            self.listener_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
            self.listener_thread.start()

    def listen_for_wake_word(self):
        while self.listener_active:
            try:
                text = get_audio(self.webcam_index)
                if WAKE in text or input("Press Enter and type 'hi' to start: ").strip().lower() == "hi":
                    print("I AM READY")
                    request = "I want a beatiful interview make up"
                    self.listener_active = False
                    self.open_magicup_app(request)
                    break
                elif BYE in text:
                    speak("Goodbye")
                    self.listener_active = False
                    self.root.quit()
                    break
            except Exception as e:
                print(f"Error while listening: {e}")
                break

    def display_text(self, index=0):
        global flash_count
        if index <= len(full_text):
            self.text_label.config(text=full_text[:index])
            self.root.after(200, self.display_text, index + 1)
        else:
            flash_count = 0
            self.flash_text()

    def flash_text(self):
        global flash_count
        if flash_count < 4:
            current_color = "black" if flash_count % 2 == 0 else "white"
            self.text_label.config(fg=current_color)
            flash_count += 1
            self.root.after(300, self.flash_text)
        else:
            self.display_text()

    def open_magicup_app(self, request):
        """Opens the MagicUpApp when the wake word is detected."""
        self.listener_active = False
        print("Opening MagicUp App")
        
        new_root = tk.Toplevel(self.root)
        MagicUpApp(new_root, request)
        self.root.withdraw()



if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
