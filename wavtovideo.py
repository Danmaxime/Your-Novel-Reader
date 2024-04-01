import sys
from moviepy.editor import *

file_name = sys.argv[1]
# Load audio and image
audio = AudioFileClip(f'{file_name}.wav')
image = ImageClip('dimensional_descent.jpeg', duration=audio.duration)

# Set audio of image clip
video = image.set_audio(audio)

# Tested and FPS does  not affect the quality of the audio
video.write_videofile(f'{file_name}.mp4', fps=1)
