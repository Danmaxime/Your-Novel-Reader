# Import necessary libraries
import os
import sys
import re
from TTS.api import TTS
import torch
import glob
from pydub import AudioSegment

# Path to your text file
text_file_path = sys.argv[1]
book_title = sys.argv[2]
split_text_file_path = os.path.splitext(text_file_path)[0]


def needs_conversion_to_system(input_string: str) -> bool:
    return input_string[0] == '[' and input_string[-2] == ']'


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Init TTS with the target model name
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(device)

# Read the text file
with open(text_file_path, 'r', encoding='utf-8') as file:
    text_line_list = file.readlines()

# Split the text into segments based on [ ] brackets
segments = []
temp_segment = ''
# Split the text into segments based on [ ] brackets
for i, item in enumerate(text_line_list):
    if (item == '' or item == '\n') and i != len(text_line_list) - 1:
        continue
    if needs_conversion_to_system(item):
        print("Is system")
        segments.append(temp_segment)
        segments.append(item)
        temp_segment = ''
        continue
    else:
        temp_segment += item

    if i == len(text_line_list) - 1:
        segments.append(temp_segment)

# Process each segment
for i, segment in enumerate(segments):
    # Determine which speaker_wav to use based on whether the segment is inside [ ] brackets
    speaker_wav = "jessica.wav" if segment[0] == '[' and segment[-2] == ']' else "nick.wav"

    # Remove [ ] brackets if present
    segment = segment.replace('[', '').replace(']', '')

    # Run TTS only if segment is not empty or does not contain only whitespace
    if segment.strip():
        tts.tts_to_file(segment, file_path=f'{split_text_file_path}_{i}.wav', speaker_wav=speaker_wav, language="en")

# Get a list of all the wav files
print("Finding wav segments")
wav_files = glob.glob(f'{split_text_file_path}_*.wav')

# Create an empty AudioSegment object
combined = AudioSegment.empty()

# Loop over each file
for wav_file in wav_files:
    print(f"Adding {wav_file} segment")
    sound = AudioSegment.from_wav(wav_file)
    combined += sound

# Export to a wav file
print("Merging wav segments")
combined.export(f"{split_text_file_path}.wav", format="wav")

for file in wav_files:
    print(f"Removing {file}")
    os.remove(file)

# Run the video script
sys.argv = ['./scripts/wav_to_video.py', f'{split_text_file_path}', f'{book_title}']
exec(open('./scripts/wav_to_video.py').read())

