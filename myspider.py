
import scrapy
import os
import re
import sys

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = []
    starting_chapter_number = 0
    next_chapter_number = 0
    ending_chapter_number = 0
    book_title = ''
    # Read the chapter number from the file
    with open('chapternumber.txt', 'r') as file:
        chapter_number = int(file.read().strip())

    # Append the URLs to the start_urls list
    for i in range(chapter_number, chapter_number + 2):
        start_urls.append(f'https://lightnovelpub.vip/novel/dimensional-descent-1216/chapter-{i}')

    # Update the chapter number in the file
    with open('chapternumber.txt', 'w') as file:
        starting_chapter_number = chapter_number
        next_chapter_number = chapter_number + 2
        ending_chapter_number = next_chapter_number - 1
        file.write(str(next_chapter_number))

    def parse(self, response):
        self.book_title = response.css('a.booktitle::text').get()
        chapter_title = response.css('span.chapter-title::text').get()
        paragraphs = response.css('div#chapter-container p::text').getall()

        # Write each chapter to a new file with the chapter number and name as the file name
        with open(f'{chapter_title}.txt', 'w') as f:
            f.write(chapter_title + '\n\n')
            for paragraph in paragraphs:
                f.write(paragraph + '\n\n')

    def close(self, reason):
        print("Spider closed: ", reason)
        print("Spider closed, running sortchapters.py")
        sys.argv = ['sortchapters.py', f'{self.book_title}', f'{self.starting_chapter_number}', f'{self.ending_chapter_number}']
        exec(open('sortchapters.py').read())
