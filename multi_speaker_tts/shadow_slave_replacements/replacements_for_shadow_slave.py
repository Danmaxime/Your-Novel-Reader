import sys
import re
import json

book_title = sys.argv[1]
starting_chapter = int(sys.argv[2])
ending_chapter = int(sys.argv[3])


def get_config():
    open_novel_list = open('novel_list.json')
    novel_list_json = json.load(open_novel_list)
    open_novel_list.close()
    path = novel_list_json[book_title.lower()]
    with open(f'{path}', 'r', encoding='utf-8') as config:
        config_obj = json.load(config)
    return config_obj


# Splits longer lines for the reader, to avoid tokenization issues
def add_newline_after_400_chars(input_string, is_system_string):
    if len(input_string) <= 400:
        return input_string

    last_space_index = input_string.rfind(' ', 0, 400)
    if not is_system_string:
        return input_string[:last_space_index] + '\n\n' + input_string[last_space_index+1:]
    else:
        return input_string[:last_space_index] + ']\n\n[' + input_string[last_space_index + 1:]


def needs_conversion_to_system(input_string: str) -> bool:
    return input_string[0] == '[' and input_string[-2] == ']'


def convert_to_system_format(input_string: str) -> str:
    remove_brackets_from_input = input_string.replace('[', '').replace(']', '')
    system_string = "[" + remove_brackets_from_input[:-1] + "]\n"
    return system_string


print("Replace for reader running")
# Open the file in read mode
with open(f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt', 'r', encoding='utf-8') as file:
    # Read all lines
    lines = file.readlines()

# Open the file in write mode
with open(f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        is_system_string = needs_conversion_to_system(line)
        if is_system_string:
            converted_to_system_string = convert_to_system_format(line)
            formatted_string = add_newline_after_400_chars(converted_to_system_string, is_system_string)
        else:
            formatted_string = add_newline_after_400_chars(line, is_system_string)

        new_line = formatted_string.replace('(+', '(Plus ').replace("\u2014", "...").replace("…", "...")
        # Write the modified line back to the file
        file.write(new_line)


multi_speaker_tts_path = get_config()['multi_speaker_tts_creator_path']
sys.argv = [multi_speaker_tts_path, f'{book_title} - Chapters {starting_chapter}-{ending_chapter}.txt', f'{book_title}']
exec(open(multi_speaker_tts_path).read())
