import sys
import os
import json
from moviepy.editor import *

file_name = sys.argv[1]
book_title = sys.argv[2]


def get_json(path):
    open_json = open(path)
    config_data = json.load(open_json)
    open_json.close()
    return config_data


print("Start WAV to video conversion")
novel_list_json = get_json('C:\\Users\\danie\\Desktop\\pyindex\\novel_list.json')
novel_config_path = novel_list_json[book_title.lower()]

novel_config = get_json(novel_config_path)

# Get the current script directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Construct the file path
file_path = os.path.join(parent_dir, f'pyindex\\{file_name}.wav')

# Load audio and image
audio = AudioFileClip(file_path)
cover_path = novel_config['cover_path']
image = ImageClip(f'{os.path.join(parent_dir, cover_path)}', duration=audio.duration)

# Set audio of image clip
video = image.set_audio(audio)

# Tested and FPS does not affect the quality of the audio
video.write_videofile(f'{file_name}.mp4', fps=1, audio_bitrate="384k")

sys.argv = ['./scripts/move_files.py', f'{file_name}', f'{book_title}']
exec(open('./scripts/move_files.py').read())
