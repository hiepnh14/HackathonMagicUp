import cv2
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import threading
import time
from imageViewer import ImageViewer
from audio import get_audio, speak, get_webcam_index
import app
import os
TAKE_PICTURE = "capture"

class MagicUpApp:
    def __init__(self, root, request=None):
        self.root = root
        self.root.title("MAGICUP")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)  # Fullscreen
        self.root.bind("<Escape>", lambda e: self.root.quit())  # Press 'Esc' to exit fullscreen
        self.request = request
        # Initialize OpenCV's face cascade classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Flags and timers
        self.face_detected = False
        self.last_face_detected_time = 0
        self.DISPLAY_DELAY = 2  # Delay time in seconds

        # Set up GUI elements
        self.camera_label = tk.Label(root, bg="black")
        self.camera_label.place(relx=0.5, rely=0.2, anchor="n")

        self.prompt_label = tk.Label(root, text="No face detected", font=("Arial", 24), fg="white", bg="black", wraplength=800, justify="center")
        self.prompt_label.place(relx=0.5, rely=0.75, anchor="n")
        # Initialize webcam audio device
        self.webcam_index = get_webcam_index()
        if self.webcam_index is None:
            print("No valid webcam audio device found. Exiting.")
            self.root.quit()
        # Start video stream
        self.cap = cv2.VideoCapture("/dev/video20")
        if not self.cap.isOpened():
            print("Error: Could not open video device.")
            return

        # Start the video stream thread
        threading.Thread(target=self.update_frame, daemon=True).start()
        self.start_listening()
        

        # Button to open the full-screen image
        app.main(image_path='image.png', file_path="generated_image.png")
        print("DONE GENERATING")
        self.open_image()

    def open_image(self, image_path = "generated_image.png"):
        # Create a new Toplevel window and show the image in full-screen
        new_window = tk.Toplevel(self.root)
        ImageViewer(new_window, image_path)

    def start_listening(self):
        """Starts listening for the wake word and other commands."""
        if self.webcam_index is not None:
            # threading.Thread(target=self.listen_for_wake_word, daemon=True).start()
            self.listen_for_wake_word()
    def listen_for_wake_word(self):
        """Continuously listens for the wake word and triggers actions accordingly."""
      
        while True:
            print("Listening...")
            text = get_audio(self.webcam_index)
            if TAKE_PICTURE in text:
                print("I AM TAKING PICTURE")
                self.take_picture()
                break

            
    def apply_rounded_corners(self, image, radius=30):
        """Applies rounded corners to the video frame."""
        rounded = Image.new("L", (image.width, image.height), 0)
        draw = ImageDraw.Draw(rounded)
        draw.rounded_rectangle((0, 0, image.width, image.height), radius=radius, fill=255)
        image.putalpha(rounded)
        return image

    def update_frame(self):
        """Updates video frame and detects faces."""
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return

        # Detect faces
        faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Check face detection state
        if len(faces) > 0:
            if not self.face_detected:
                self.face_detected = True
                self.prompt_label.config(text="Your face has been detected. Do you want to take a photo and generate today's makeup?")
            self.last_face_detected_time = time.time()
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            if self.face_detected and (time.time() - self.last_face_detected_time) > self.DISPLAY_DELAY:
                self.face_detected = False
                self.prompt_label.config(text="No face detected")

        # Convert image to RGB, apply rounded corners, and display in Tkinter
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        img = self.apply_rounded_corners(img, radius=30)
        img_tk = ImageTk.PhotoImage(image=img)

        self.camera_label.img_tk = img_tk  # Prevent garbage collection
        self.camera_label.config(image=img_tk)

        # Schedule the next frame update
        self.root.after(50, self.update_frame)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
    def take_picture(self):
        """Takes a picture from the video stream and saves it as an image file."""
        ret, frame = self.cap.read()
        if ret:
            filename = "image.png"
            # Save the current frame as an image file
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Existing file {filename} removed.")
            
            cv2.imwrite(filename, frame)
            print(f"Image saved as {filename}")

# Create the main Tkinter window and run the application
# root = tk.Tk()
# app = MagicUpApp(root)
# root.mainloop()

