import os
import re
import sys
import shutil
import json
import scrapy
from TTS.api import TTS
import torch
from moviepy.editor import *

class MySpider(scrapy.Spider):
    name = 'my_spider'
    grab_count = 0

    @staticmethod
    def get_chapter_grab_count(path):
        with open(f'{path}', 'r', encoding='utf-8') as config:
            config_obj = json.load(config)
        chapter_grab_count = int(config_obj['chapter_grab_count'])
        return chapter_grab_count

    @staticmethod
    def get_config(path):
        with open(f'{path}', 'r', encoding='utf-8') as config:
            config_obj = json.load(config)
        return config_obj

    def start_requests(self):
        open_json = open('novel_list.json')
        config_data = json.load(open_json)
        open_json.close()

        valid_novel_config_list = [config_data[novel] for novel in config_data if os.path.isfile(config_data[novel])]

        for valid_config in valid_novel_config_list:
            with open(f'{valid_config}', 'r', encoding='utf-8') as config:
                config_obj = json.load(config)

            book_title = config_obj['book_title']
            starting_chapter_number = config_obj['next_chapter_num']
            book_base_url = config_obj['book_base_url']
            chapter_grab_count = self.get_chapter_grab_count(valid_config)
            next_chapter_number = starting_chapter_number + chapter_grab_count
            for i in range(starting_chapter_number, next_chapter_number):
                is_last_request = i == next_chapter_number - 1
                yield scrapy.Request(f'{book_base_url}{i}', self.parse,
                                     cb_kwargs={'config_path': valid_config, 'next_chapter_number': next_chapter_number,
                                                'book_title': book_title,
                                                'starting_chapter_number': starting_chapter_number,
                                                'is_last_request': is_last_request})

    def parse(self, response, config_path, next_chapter_number, book_title, starting_chapter_number, is_last_request):
        self.grab_count = self.grab_count + 1
        chapter_title = response.css('span.chapter-title::text').get()
        paragraphs = response.css('div#chapter-container p::text').getall()
        title_parts = chapter_title.split(":")

        with open(f'{book_title} - {title_parts[0]}.txt', 'w', encoding='utf-8') as f:
            f.write(chapter_title + '\n\n')
            for paragraph in paragraphs:
                f.write(paragraph + '\n\n')

        needed_grab_count = int(self.get_config(config_path)['chapter_grab_count'])

        if self.grab_count == needed_grab_count:
            self.grab_count = 0
            with open(f'{config_path}', 'r', encoding='utf-8') as config:
                config_obj = json.load(config)

            with open(f'{config_path}', 'w', encoding='utf-8') as config:
                config_obj['next_chapter_num'] = next_chapter_number
                json.dump(config_obj, config, indent=4)

            print("All requests for this config have been processed, running sort_chapters.py")
            sys.argv = ['./scripts/sort_chapters.py', f'{book_title}', f'{starting_chapter_number}',
                        f'{next_chapter_number}']
            exec(open('./scripts/sort_chapters.py').read())
