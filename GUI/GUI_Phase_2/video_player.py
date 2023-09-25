from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip
import sensor_data
import time

def play_video(root, video_label, sensor_label, pothole_status_label, overflow_status_label):
    video_path = r"D:\Project Codes\IOTSA\sewagedetector\GUI\GUI_Phase_2\Welcome.mp4"  # Updated video file path
    clip = VideoFileClip(video_path)

    # Get the video resolution
    video_width, video_height = clip.size

    # Set the window size to match the video resolution
    root.geometry(f"{video_width}x{video_height}")

    for frame in clip.iter_frames(fps=15):  # Reduced frame rate
        frame = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=frame)
        video_label.config(image=photo)
        video_label.image = photo
        root.update_idletasks()
    
    # Delay for a few seconds before switching to sensor data (adjust as needed)
    time.sleep(5)
    
    # After video ends, remove the video and show sensor data
    video_label.pack_forget()
    sensor_label.pack()
    pothole_status_label.pack()
    overflow_status_label.pack()
    
    # Start updating sensor data
    while True:
        sensor_data.update_sensor_data(sensor_label, pothole_status_label, overflow_status_label)
        time.sleep(1)  # Update sensor data every 1 second (adjust as needed)