import sys
import re
book_title = sys.argv[1]
starting_chapter = int(sys.argv[2])
ending_chapter = int(sys.argv[3])


def add_newline_after_400_chars(input_string):
    if len(input_string) > 400:
        last_space_index = input_string.rfind(' ', 0, 400)
        return input_string[:last_space_index] + '\n\n' + input_string[last_space_index+1:]
    else:
        return input_string


print("Replace for reader running")
# Open the file in read mode
with open(f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt', 'r', encoding='utf-8') as file:
    # Read all lines
    lines = file.readlines()

# Open the file in write mode
with open(f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        # Replace '(+' with '(Plus '
        new_line = line.replace('(+', '(Plus ').replace("\u2014", "...").replace("…", "...")
        new_line = add_newline_after_400_chars(new_line)
        # Write the modified line back to the file
        file.write(new_line)

sys.argv = ['./scripts/ttscreator.py', f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt', f'{book_title}']
exec(open('./scripts/ttscreator.py').read())