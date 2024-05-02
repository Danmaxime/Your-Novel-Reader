import os
import glob
import re
import sys
import json

# Get the command line arguments
book_title = sys.argv[1]
starting_chapter = int(sys.argv[2])
ending_chapter = int(sys.argv[3]) - 1


def get_config():
    open_novel_list = open('novel_list.json')
    novel_list_json = json.load(open_novel_list)
    open_novel_list.close()
    path = novel_list_json[sys.argv[1].lower()]
    with open(f'{path}', 'r', encoding='utf-8') as config:
        config_obj = json.load(config)
    return config_obj

print("sort_chapters.py is running")
# script to sort the chapters in the CWD and append them to one another in a new 
# .txt file in the correct order 
chapter_list = []
for file in glob.glob("*.txt"):
    chapter_list.append(file)


for chapter in chapter_list.copy():
    if chapter[0:7] != "Chapter":
        chapter_list.remove(chapter)

# Extract the chapter number and sort based on it
chapter_list.sort(key=lambda fname: int(re.search(r'\d+', fname).group()))

with open(f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt', 'a', encoding='utf-8', errors='ignore') as outfile:
    for fname in chapter_list:
        with open(fname, 'r', encoding='utf-8') as infile:
            for line in infile:
                outfile.write(line)

print(chapter_list)
for chapter in chapter_list:
    os.remove(chapter)

novel_config = get_config()
if bool(novel_config['is_multi_speaker']):
    print(f"\nIs multi reader\n{book_title}\n{starting_chapter}\n{ending_chapter}")
    sys.argv = [novel_config['replace_for_reader_path'], f'{book_title}', f'{starting_chapter}', f'{ending_chapter}']
    exec(open(novel_config['replace_for_reader_path']).read())
else:
    print(f"\nIs regular reader\n{book_title}\n{starting_chapter}\n{ending_chapter}")
    sys.argv = ['./scripts/replace_for_reader.py', f'{book_title}', f'{starting_chapter}', f'{ending_chapter}']
    exec(open('./scripts/replace_for_reader.py').read())
