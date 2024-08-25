import os
import numpy as np
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image

# Function to edit video with a background frame
def edit_video(video_path, background_image_path, output_path):
    try:
        # Load the video clip
        video_clip = VideoFileClip(video_path)

        # Load the image as a background frame
        background_frame_pil = Image.open(background_image_path)

        # Resize the background frame using Pillow
        background_frame_pil = background_frame_pil.resize((video_clip.w, video_clip.h), resample=Image.LANCZOS)

        # Convert the Pillow image to a NumPy array
        background_frame = np.array(background_frame_pil)

        # Ensure the background frame has three color channels
        if background_frame.ndim == 2:
            background_frame = np.stack([background_frame] * 3, axis=-1)

        # Set the duration of the background frame
        background_frame = ImageClip(background_frame).set_duration(video_clip.duration)

        # Position the background frame at the center
        background_frame = background_frame.set_position(('center', 'center'))

        # Position the video at the center
        video_clip = video_clip.set_position(('center', 'center'))

        # Overlay the video on the background frame
        final_clip = CompositeVideoClip([background_frame, video_clip])

        # Save the final video with the added background frame in the same folder
        final_clip.write_videofile(output_path, codec='libx264', fps=60)

        print(f"Video edited successfully: {output_path}")
    except Exception as e:
        print(f"Error editing video {video_path}: {e}")

# Directory containing folders with videos
root_directory = '/sdcard/insta'

# Iterate through each folder and process videos
for foldername, subfolders, filenames in os.walk(root_directory):
    for filename in filenames:
        # Check if the file is a video and not already edited
        if filename.endswith(('.mp4', '.avi', '.mov')) and not filename.startswith('edited_'):
            video_file = os.path.join(foldername, filename)
            background_image = '/sdcard/insta/background.jpg'
            output_file = os.path.join(foldername, f'edited_{filename}')

            # Edit the video and save it in the same folder
            edit_video(video_file, background_image, output_file)
