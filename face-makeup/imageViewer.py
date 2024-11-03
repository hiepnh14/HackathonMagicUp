import tkinter as tk
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, master, image_path):
        self.master = master
        self.master.title("Full-Screen Image")
        self.master.attributes("-fullscreen", True)  # Set window to full-screen
        self.master.configure(bg="black")

        # Bind the Escape key to exit full-screen
        self.master.bind("<Escape>", lambda e: self.master.destroy())

        # Load and display the image in full screen
        self.display_image(image_path)

    def display_image(self, image_path):
        # Load the image
        img = Image.open(image_path)
        # Resize the image to fit the screen dimensions
        img = img.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        # Display the image in a label
        img_label = tk.Label(self.master, image=img_tk, bg="black")
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.pack(expand=True)
