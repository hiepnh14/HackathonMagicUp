import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from audio import get_audio, speak, get_webcam_index, record_speech  # Make sure audio functions are in audio.py
from mainUI import MagicUpApp  # Ensure MagicUpApp is defined in magicup_app.py
import threading
# Paths to the GIF files
gif_path = "pic/face-makeup.gif"
mic_gif_path = "pic/microphone-recording.gif"  # Path to the microphone GIF icon

WAKE = "hi"
BYE = "bye"
# Text to display
full_text = "ARE YOU READY TO BE BEAUTIFUL?"
# Create a frame to hold the GIF and text, centered and adaptive


# Variables for controlling the text animation
flash_count = 0  # Counter to control the number of flashes

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MAGICUP")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)  # Set window to fullscreen
        self.root.bind("<Escape>", lambda e: self.root.quit())  # Press 'Esc' to exit fullscreen
        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(expand=True)
        # Create a label to display text below the GIF, aligned to the left
        self.text_label = tk.Label(self.frame, font=("Arial", 30), fg="white", bg="black", anchor="w", justify="left")
        self.text_label.pack(fill="x", padx=20)  # Left-aligned text with padding
        # Initialize webcam audio device
        self.webcam_index = get_webcam_index()
        if self.webcam_index is None:
            print("No valid webcam audio device found. Exiting.")
            self.root.quit()

        # Create the main frame
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True)

        # Set up main GIF animation
        self.setup_gif_animation()

        self.display_text()
        # Set up microphone icon animation
        self.setup_microphone_icon()

        # Label for the microphone prompt text
        self.prompt_label = tk.Label(self.mic_frame, text="Try to say: 'Hi' to start! And tell me what makeup do you want!", 
                                     font=("Arial", 20), fg="white", bg="black")
        self.prompt_label.pack(side="left")

        # Start listening for wake word
        self.start_listening()

    def setup_gif_animation(self):
        """Sets up the main GIF animation and its label."""
        gif_image = Image.open(gif_path)
        new_size = (int(gif_image.width * 0.7), int(gif_image.height * 0.7))
        self.frames = [ImageTk.PhotoImage(frame.copy().resize(new_size, Image.LANCZOS)) for frame in ImageSequence.Iterator(gif_image)]
        self.frame_index = 0
        self.gif_label = tk.Label(self.frame, bg="black")
        self.gif_label.pack(pady=20)  # Place the GIF label with padding
        self.update_gif()  # Start GIF animation

    def update_gif(self):
        """Updates the GIF animation on the main window."""
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.gif_label.config(image=self.frames[self.frame_index])
        self.root.after(int(100), self.update_gif)

    def setup_microphone_icon(self):
        """Sets up the microphone icon animation at the bottom of the screen."""
        mic_image = Image.open(mic_gif_path)
        mic_new_size = (int(mic_image.width * 0.1), int(mic_image.height * 0.1))
        self.mic_frames = [ImageTk.PhotoImage(frame.copy().resize(mic_new_size, Image.LANCZOS)) for frame in ImageSequence.Iterator(mic_image)]
        self.mic_frame_index = 0

        # Microphone frame
        self.mic_frame = tk.Frame(self.root, bg="black")
        self.mic_frame.pack(side="bottom", pady=10)
        self.mic_label = tk.Label(self.mic_frame, bg="black")
        self.mic_label.pack(side="left", padx=(0, 10))
        self.update_mic_gif()  # Start microphone icon animation

    def update_mic_gif(self):
        """Updates the microphone GIF animation."""
        self.mic_frame_index = (self.mic_frame_index + 1) % len(self.mic_frames)
        self.mic_label.config(image=self.mic_frames[self.mic_frame_index])
        self.root.after(int(100), self.update_mic_gif)

    def start_listening(self):
        """Starts listening for the wake word and other commands."""
        if self.webcam_index is not None:
            threading.Thread(target=self.listen_for_wake_word, daemon=True).start()
            # self.listen_for_wake_word()
    def listen_for_wake_word(self):
        """Continuously listens for the wake word and triggers actions accordingly."""
      
        while True:
            print("Listening...")
            text = get_audio(self.webcam_index)
            if WAKE in text:
                print("I AM READY")
                
                request = record_speech()
                self.open_magicup_app(request = request)
                break

            elif BYE in text:
                speak("Goodbye")
                self.root.quit()
                break
                
    def display_text(self, index=0):
        global flash_count
        if index <= len(full_text):
            self.text_label.config(text=full_text[:index])  # Update the text up to the current index
            root.after(200, self.display_text, index + 1)  # Schedule the next letter (adjust speed as needed)
        else:
            # Start flashing after the text is fully displayed
            self.flash_count = 0
            self.flash_text()

    # Function to flash the text twice
    def flash_text(self):
        global flash_count
        if flash_count < 4:  # Flash twice (each flash consists of two states: visible and invisible)
            current_color = "black" if flash_count % 2 == 0 else "white"
            self.text_label.config(fg=current_color)
            flash_count += 1
            root.after(300, self.flash_text)  # Control the speed of the flash
        else:
            # Restart the gradual text display after flashing
            self.display_text()

    def open_magicup_app(self, request):
        """Opens the MagicUpApp when the wake word is detected."""
        
        print("What the hell")
        new_root = tk.Toplevel(self.root)
        MagicUpApp(new_root, request)
        # self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk, ImageSequence
# from audio import get_audio, speak, get_webcam_index
# # Paths to the GIF files
# gif_path = "pic/face-makeup.gif"
# mic_gif_path = "pic/microphone-recording.gif"  # Path to the microphone GIF icon

# # Create the main window
# root = tk.Tk()
# root.title("MAGICUP")
# root.configure(bg="black")
# root.attributes("-fullscreen", True)  # Set window to fullscreen
# root.bind("<Escape>", lambda e: root.quit())  # Press 'Esc' to exit fullscreen

# # Create a frame to hold the GIF and text, centered and adaptive
# frame = tk.Frame(root, bg="black")
# frame.pack(expand=True)

# # Load the main GIF animation and resize each frame
# gif_image = Image.open(gif_path)
# original_width, original_height = gif_image.size
# new_size = (int(original_width * 0.7), int(original_height * 0.7))  # Scale down by 30%
# frames = [ImageTk.PhotoImage(frame.copy().resize(new_size, Image.LANCZOS)) for frame in ImageSequence.Iterator(gif_image)]
# frame_index = 0

# # Create a label to display the main GIF
# gif_label = tk.Label(frame, bg="black")
# gif_label.pack(pady=20)  # Place the GIF label with padding

# # Update the main GIF frames with increased speed
# def update_gif():
#     global frame_index
#     frame_index = (frame_index + 1) % len(frames)  # Loop through frames
#     gif_label.config(image=frames[frame_index])
# #     root.after(int(gif_image.info['duration'] / 1.5), update_gif)  # Increase speed by 50%

# # # Start the main GIF animation
# # update_gif()

# # # Create a label to display text below the GIF, aligned to the left
# # text_label = tk.Label(frame, font=("Arial", 30), fg="white", bg="black", anchor="w", justify="left")
# # text_label.pack(fill="x", padx=20)  # Left-aligned text with padding

# # # Text to display
# # full_text = "ARE YOU READY TO BE BEAUTIFUL?"

# # # Variables for controlling the text animation
# # flash_count = 0  # Counter to control the number of flashes

# # # Function to display text gradually
# # def display_text(index=0):
# #     global flash_count
# #     if index <= len(full_text):
# #         text_label.config(text=full_text[:index])  # Update the text up to the current index
# #         root.after(200, display_text, index + 1)  # Schedule the next letter (adjust speed as needed)
# #     else:
# #         # Start flashing after the text is fully displayed
# #         flash_count = 0
# #         flash_text()

# # # Function to flash the text twice
# # def flash_text():
# #     global flash_count
# #     if flash_count < 4:  # Flash twice (each flash consists of two states: visible and invisible)
# #         current_color = "black" if flash_count % 2 == 0 else "white"
# #         text_label.config(fg=current_color)
# #         flash_count += 1
# #         root.after(300, flash_text)  # Control the speed of the flash
# #     else:
# #         # Restart the gradual text display after flashing
# #         display_text()

# # # Start displaying the text gradually
# # display_text()

# # # Load microphone GIF icon and create frames with reduced size (50% smaller)
# # mic_image = Image.open(mic_gif_path)
# # mic_original_width, mic_original_height = mic_image.size
# # mic_new_size = (int(mic_original_width * 0.1), int(mic_original_height * 0.1))  # Reduce size by 50%
# # mic_frames = [ImageTk.PhotoImage(frame.copy().resize(mic_new_size, Image.LANCZOS)) for frame in ImageSequence.Iterator(mic_image)]
# # mic_frame_index = 0

# # # Create a frame to hold the microphone GIF and prompt text side by side, anchored at the bottom
# # mic_frame = tk.Frame(root, bg="black")
# # mic_frame.pack(side="bottom", pady=10)  # Place at the bottom with padding

# # # Create a label to display the microphone GIF icon inside mic_frame
# # mic_label = tk.Label(mic_frame, bg="black")
# # mic_label.pack(side="left", padx=(0, 10))  # Add space between icon and text

# # # Function to update microphone GIF frames
# # def update_mic_gif():
# #     global mic_frame_index
# #     mic_frame_index = (mic_frame_index + 1) % len(mic_frames)  # Loop through frames
# #     mic_label.config(image=mic_frames[mic_frame_index])
# #     root.after(int(mic_image.info['duration']), update_mic_gif)

# # # Start the microphone GIF animation
# # update_mic_gif()

# # # Label for prompt text next to the microphone icon inside mic_frame
# # prompt_label = tk.Label(mic_frame, text="Try to say: 'Hi Mirror' to start!", font=("Arial", 20), fg="white", bg="black")
# # prompt_label.pack(side="left")

# # # Run the main loop
# # root.mainloop()


# # WAKE = "hi"
# # BYE = "bye"

# # # Get the WebCam device index
# # webcam_index = get_webcam_index()

# # if webcam_index is not None:
# #     while True:
# #         print("Listening...")
# #         text = get_audio(webcam_index)
# #         if WAKE in text:
# #             # speak("I am ready")
            
# #             print("I am ready")
            
# #             text = get_audio(webcam_index)
# #         if BYE in text:
# #             speak("Goodbye")
# #             break
# # else:
# #     print("No valid webcam audio device found. Exiting.")