import os
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def html_section_exists(section_name):
    return os.path.isfile(f'raw_html/{section_name}.html')


def extract_html(url, section_name):
    if not html_section_exists(section_name):
        options = Options()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        element = driver.find_element(By.CLASS_NAME, 'js-article-content')
        html = str(element.get_attribute('innerHTML'))
        # with open(f'raw/{section_name}.html', 'w') as file:
        #     file.write(html)

        html = trim_content(html)
        images = driver.find_elements(By.TAG_NAME, 'img')
        html = replace_ext_images(html, images)

        with open(f'raw_html/{section_name}.html', 'w') as file:
            file.write(html)
        
        with open('raw_html/book.html', 'a') as file:
            file.write(html)
    else:
        with open(f'raw_html/{section_name}.html') as file:
            html = file.read()

    chapters = section_name.split("-")
    chapters_html = split_chapters(html, len(chapters))

    for i in range(len(chapters_html)):
        yield (chapters[i], chapters_html[i])


def trim_content(html):
    html_lines = html.splitlines()
    block_spacer_indices = [i for i in range(len(html_lines)) if 'wp-block-spacer' in html_lines[i]]
    html_lines = html_lines[block_spacer_indices[0]:block_spacer_indices[-2]]
    return "\n".join(html_lines)


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

def split_chapters(html, num_chapters):
    if num_chapters == 1:
        return [html]
    
    chapters = []
    html_lines = html.splitlines()
    chapter_indices = [i for i in range(len(html_lines)) if chapter_match(html_lines[i])]

    if len(chapter_indices) == num_chapters:
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
    else:
        print('No matching chapters found!!!')
        chapters = html
    
    return chapters

def chapter_match(line):
    if 'wp-block-heading' in line:
        if 'Chapter' in line or 'Prologue' in line or 'Preface' in line or 'Interlude' in line:
            return True
    return False
