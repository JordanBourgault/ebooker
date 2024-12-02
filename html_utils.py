import os
import requests
import re
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def create_dirs():
    Path("./static").mkdir(parents=True, exist_ok=True)
    Path("./raw_html").mkdir(parents=True, exist_ok=True)


def html_section_exists(section_name):
    return os.path.isfile(f'raw_html/{section_name}.html')


def extract_html(url):
    create_dirs()
    section_name = url.split('/')[-2]
    if not html_section_exists(section_name):
        options = Options()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        element = driver.find_element(By.CLASS_NAME, 'js-article-content')
        html = str(element.get_attribute('innerHTML'))

        html = trim_content(html)
        images = driver.find_elements(By.TAG_NAME, 'img')
        html = replace_ext_images(html, images)

        with open(f'raw_html/{section_name}.html', 'w', encoding='utf-8') as file:
            file.write(html)
        
        with open('raw_html/book.html', 'a', encoding='utf-8') as file:
            file.write(html)
    else:
        with open(f'raw_html/{section_name}.html', encoding='utf-8') as file:
            html = file.read()

    chapters_html, chapters_titles = split_chapters(html)

    for i in range(len(chapters_html)):
        yield (chapters_titles[i], chapters_html[i])


def trim_content(html):
    html_lines = html.splitlines()
    block_separator_indices = [i for i in range(len(html_lines)) if 'wp-block-separator' in html_lines[i]]
    html_lines = html_lines[block_separator_indices[0]:block_separator_indices[-1]-2]
    remove_bad_newlines(html_lines)
    return "\n".join(html_lines)


def remove_bad_newlines(html_lines):
    offset = 0
    i = 0
    while i < len(html_lines) - offset:
        index = i + offset
        if html_lines[index][0] != '<':
            html_lines[index-1] += html_lines[index]
            html_lines.pop(index)
            offset += 1
        i += 1


def replace_ext_images(html, images):
    for image in images:
        src = image.get_attribute('src')
        if src:
            img_name = src.split('/')[-1]
            if not os.path.isfile(f'./static/{img_name}') and src.split(':')[0] == 'https':
                res = requests.get(src)
                with open(f'./static/{img_name}', 'wb') as handler:
                    handler.write(res.content)

            html = html.replace(src, f'./static/{img_name}')
    return html

def split_chapters(html):
    chapters = []
    html_lines = html.splitlines()
    chapter_indices = [i for i in range(len(html_lines)) if chapter_match(html_lines[i])]
    chapter_names = []
    for index in chapter_indices:
        line = html_lines[index]
        chapter_title = re.split('>|<', line)[2]
        chapter_names.append(chapter_title)

    # First chapter
    chapter_html = html_lines[0:chapter_indices[1]-1]
    chapters.append("\n".join(chapter_html))

    # Middle chapters
    if len(chapter_indices) > 2:
        for i in range(1, len(chapter_indices) - 1):
            chapter_html = html_lines[chapter_indices[i]-1:chapter_indices[i+1]-2]
            chapters.append("\n".join(chapter_html))
    
    # Last chapter
    chapter_html = html_lines[chapter_indices[-1]-1:]
    chapters.append("\n".join(chapter_html))

    return chapters, chapter_names

def chapter_match(line):
    keywords = ['Chapter', 'Prologue', 'Preface', 'Interlude', 'Day', 'Dedication']
    if 'wp-block-heading' in line and 'h3' in line:
        if any(keyword in line for keyword in keywords):
            return True
    return False
