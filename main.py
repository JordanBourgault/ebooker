from html_utils import extract_html, create_dirs
from book_utils import epubBook

chapters = [
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-preface-and-prologue/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-1-and-2/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-3-and-4/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-5-and-6/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-7-8-and-9/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-10-and-11/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-12-and-13/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-interludes-1-and-2/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-14-and-15/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-16-17-and-18/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-19-and-20/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-21-and-22/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-23-and-24/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-25-and-26/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-27-and-28/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-29-and-30/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapters-31-and-32/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-chapter-33/",
    "https://reactormag.com/read-wind-and-truth-by-brandon-sanderson-interludes-3-and-4/"
]

book = epubBook()
for url in chapters:
    chapters = extract_html(url)
    for chapter in chapters:
        book.write_chapter(chapter[0], chapter[1])

book.publish_book('Wind and Truth')
