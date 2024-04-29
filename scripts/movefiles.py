import shutil
import sys

file_name = sys.argv[1]
book_title = sys.argv[2]

formatted_name_for_dir = book_title.lower().replace(' ', '_')

# specify destination directory
dest_dir = f'Z:\\Novel_Reader\\{formatted_name_for_dir}'

# move file to new directory
shutil.move(f'{file_name}.mp4', f'{dest_dir}\\MP4\\{file_name}.mp4')
shutil.move(f'{file_name}.txt', f'{dest_dir}\\TXT\\{file_name}.txt')
shutil.move(f'{file_name}.wav', f'{dest_dir}\\WAV\\{file_name}.wav')
