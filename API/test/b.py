import tkinter as tk
from PIL import Image, ImageTk
import threading
from ollama import chat, ChatResponse
import time

# Animation states
MODES = {
    "speak": [
        "../QR_Codes/F_IMG/1.png",
        "../QR_Codes/F_IMG/2.png",
        "../QR_Codes/F_IMG/3.png",
    ],
    "idle": [
        "../QR_Codes/F_IMG/4.png",
        "../QR_Codes/F_IMG/5.png",
        "../QR_Codes/F_IMG/6.png",
    ],
    "work": [
        "../QR_Codes/F_IMG/7.png",
        "../QR_Codes/F_IMG/8.png",
        "../QR_Codes/F_IMG/9.png",
    ]
}

current_mode = "idle"  # Default mode
current_frame_index = 0
images = {}  # Cache for loaded images
is_processing = False  # Flag to track processing state


# Load images for all modes
def load_images():
    for mode, paths in MODES.items():
        images[mode] = [ImageTk.PhotoImage(Image.open(path)) for path in paths]


# Update animation frame
def update_frame():
    global current_frame_index
    frame_list = images[current_mode]
    frame_count = len(frame_list)

    # Update the displayed image
    frame = frame_list[current_frame_index]
    image_label.config(image=frame)
    current_frame_index = (current_frame_index + 1) % frame_count

    # Schedule the next frame update
    root.after(800, update_frame)  # Delay of 800ms


# Handle user input from terminal, call AI, and animate
def process_input_from_terminal():
    global current_mode, is_processing

    while True:
        # Display prompt in terminal
        print("Type your question (or type 'exit' to quit): ", end="", flush=True)
        user_input = input()

        if user_input.lower() == "exit":
            root.destroy()
            break

        # Set mode to 'work' while processing
        current_mode = "work"

        # Background thread to process input
        def background_task():
            global current_mode, is_processing
            is_processing = True
            try:
                # Call AI model
                response: ChatResponse = chat(model="llama3.2", messages=[
                    {'role': 'user', 'content': user_input}
                ])
                answer = response.message.content

                # Update terminal with AI response
                print(f"AI Response: {answer}")

                # Switch to 'speak' mode after response
                current_mode = "speak"

                # Return to 'idle' after 3 seconds
                time.sleep(3)
                current_mode = "idle"
            except Exception as e:
                print(f"Error: {e}")
                current_mode = "idle"
            finally:
                is_processing = False

        threading.Thread(target=background_task, daemon=True).start()


# Create the Tkinter window
root = tk.Tk()
root.title("AI Animation Example")

# Load images before starting
load_images()

# Label to display animation frames
image_label = tk.Label(root)
image_label.pack()

# Start the animation loop
update_frame()

# Start the user input loop in a separate thread
threading.Thread(target=process_input_from_terminal, daemon=True).start()

# Run the Tkinter main loop
root.mainloop()
