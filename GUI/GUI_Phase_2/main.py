import tkinter as tk
from tkinter import ttk
import threading
import sensor_data
import video_player

# Declare global variables
video_label = None
sensor_label = None
pothole_status_label = None
overflow_status_label = None

def skip_intro():
    global video_label, sensor_label, pothole_status_label, overflow_status_label
    if video_label:
        # Hide the video label
        video_label.pack_forget()
    
    # Show sensor data labels
    sensor_label.pack(anchor="w")  # Left-align sensor data
    pothole_status_label.pack(anchor="w")  # Left-align pothole status
    overflow_status_label.pack(anchor="w")  # Left-align overflow status
    
    # Start sensor data updates immediately (remove the delay)
    sensor_data.update_sensor_data(sensor_label, pothole_status_label, overflow_status_label)

def main():
    global video_label, sensor_label, pothole_status_label, overflow_status_label  # Declare global variables
    
    # Create the main application window with video resolution
    root = tk.Tk()
    root.title("Sensor Data Display")
    root.geometry("1920x1080")  # Set the window size to match the video resolution

    # Change the background color of the main window to #FBC236
    root.configure(bg="#FBC236")

    # Create global labels for sensor data (initially hidden)
    sensor_label = tk.Label(root, text="Sensor Data: N/A", font=("Atma", 40, "bold"), anchor="w", background="#FBC236")
    pothole_status_label = tk.Label(root, text="Pot Hole Status: N/A", font=("Atma", 30, "bold"), anchor="w", background="#FBC236")
    overflow_status_label = tk.Label(root, text="Overflow: N/A", font=("Atma", 30, "bold"), anchor="w", background="#FBC236")

    # Create a label to display the video
    video_label = ttk.Label(root)
    video_label.pack()

    # Add an exception button to skip the intro and start sensor data updates
    skip_button = tk.Button(root, text="Skip Intro", command=skip_intro)
    skip_button.place(x=10, y=10)  # Adjust the position as needed

    # Start video playback in a separate thread
    video_thread = threading.Thread(target=video_player.play_video, args=(root, video_label, sensor_label, pothole_status_label, overflow_status_label))
    video_thread.daemon = True
    video_thread.start()

    # Start the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
