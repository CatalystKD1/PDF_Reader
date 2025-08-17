import pyttsx3
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter.filedialog import askopenfilename
import threading

# Create main Tkinter window
root = tk.Tk()
root.title("PDF Reader")
root.geometry("300x200")

# Ask user to select a PDF
book = askopenfilename(title="Select a PDF", filetypes=[("PDF files", "*.pdf")])
pdfreader = None
pages = 0

if book:
    pdfreader = PdfReader(book)
    pages = len(pdfreader.pages)

player = pyttsx3.init()
reading_thread = None
is_reading = False

def read_pdf():
    global reading_thread, is_reading
    if pdfreader and not is_reading:
        is_reading = True
        status_label.config(text="Reading...")

        def task():
            for num in range(pages):
                page = pdfreader.pages[num]
                text = page.extract_text()
                if text:
                    player.say(text)
            player.runAndWait()
            reset_state()

        reading_thread = threading.Thread(target=task, daemon=True)
        reading_thread.start()
    else:
        status_label.config(text="No PDF selected or already reading!")

def stop_reading():
    global is_reading
    if is_reading:
        player.stop()
        reset_state()

def reset_state():
    global is_reading
    is_reading = False
    status_label.config(text="Stopped or finished reading.")

# UI elements
label = tk.Label(root, text="Click a button to control reading.", font=("Arial", 12))
label.pack(pady=10)

read_button = tk.Button(root, text="Read PDF", command=read_pdf, font=("Arial", 12))
read_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Reading", command=stop_reading, font=("Arial", 12), fg="red")
stop_button.pack(pady=5)

status_label = tk.Label(root, text="", font=("Arial", 10), fg="blue")
status_label.pack(pady=5)

# Start Tkinter event loop
root.mainloop()
