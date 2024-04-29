# Import necessary libraries
import os
import sys
from TTS.api import TTS
import torch

text_file_path = sys.argv[1]
book_title = sys.argv[2]
split_text_file_path = os.path.splitext(text_file_path)[0]

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Init TTS with the target model name
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)

with open(text_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Run TTS
tts.tts_to_file(text, file_path=f'{split_text_file_path}.wav', speaker_wav="nick.wav", language="en")

sys.argv = ['./scripts/wavtovideo.py', f'{split_text_file_path}', f'{book_title}']
exec(open('./scripts/wavtovideo.py').read())
