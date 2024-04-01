# Import necessary libraries
import os
import sys
from TTS.api import TTS
import torch


# Path to your text file
text_file_path = sys.argv[1]
#text_file_path = "Dimensional Descent - Chapters 6-7.txt"
split_text_file_path = os.path.splitext(text_file_path)[0]

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Init TTS with the target model name
#tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to(device)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)


# Read the text file
with open(text_file_path, 'r') as file:
    text = file.read()

# Run TTS
tts.tts_to_file(text, file_path=f'{split_text_file_path}.wav', speaker_wav="nick.wav", language="en")

sys.argv = ['wavtovideo.py', f'{split_text_file_path}']
exec(open('wavtovideo.py').read())
