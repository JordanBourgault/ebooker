from html_utils import extract_html
from book_utils import epubBook

chapters = {
    "Preface-Prologue": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-preface-and-prologue/",
    "1-2": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-1-and-2/",
    "3-4": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-3-and-4/",
    "5-6": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-5-and-6/",
    "7-8-9": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-7-8-and-9/",
    "10-11": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-10-and-11/",
    "12-13": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-12-and-13/",
    "Interlude 1-Interlude 2": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-interludes-1-and-2/",
    "14-15": "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-14-and-15/"
}

book = epubBook()
for section, url in chapters.items():
    chapters = extract_html(url, section)
    for chapter in chapters:
        book.write_chapter(chapter[0], chapter[1])

book.publish_book('Wind and Truth')
