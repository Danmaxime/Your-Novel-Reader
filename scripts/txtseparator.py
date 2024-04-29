def generate_files(source_file):
    with open(source_file, 'r') as file:
        content = file.read()
        i = 2
        while True:
            start = content.find(f'Chapter {i}')
            end = content.find(f'Chapter {i+2}')
            if start == -1:
                break
            if end == -1:
                end = len(content)
            chapter_content = content[start:end]
            with open(f'Dimensional Descent - Chapters {i}-{i+1}.txt', 'w') as output_file:
                output_file.write(chapter_content)
            i += 2

# Call the function with the path to your source file
generate_files('Dimensional Descent - Chapters 1-40.txt')
