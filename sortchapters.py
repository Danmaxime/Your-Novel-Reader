import os
import glob
import re
import sys

# Get the command line arguments
book_title = sys.argv[1]
starting_chapter = int(sys.argv[2])
ending_chapter = int(sys.argv[3])

print("sortchapters.py is running")
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

with open(f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt', 'a') as outfile:
    for fname in chapter_list:
        with open(fname, 'r') as infile:
            for line in infile:
                # searches for an open parentheses followed by a '+' and changes the text within the parentheses into ("Plus" x.x)
                line = re.sub(r'\((\+)', r'(Plus ', line)
                outfile.write(line)

for chapter in chapter_list:
    os.remove(chapter)
    sys.argv = ['ttscreator.py', f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt']
    exec(open('ttscreator.py').read())
