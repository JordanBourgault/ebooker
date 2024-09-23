from ebooklib import epub
import os


class epubBook:
    def __init__(self):
        self.book = epub.EpubBook()
        self.set_info()

    def set_info(self):
        self.book.set_cover('static/Wind-and-Truth_cover-small.jpg', open('./static/Wind-and-Truth_cover-small.jpg', 'rb').read())
        self.book.set_identifier("id123456")
        self.book.set_title("Wind and Truth")
        self.book.set_language("en")
        self.book.add_author("Brandon Sanderson")
        self.book.spine = ["nav"]
    
    def add_toc(self):
        self.book.toc = (self.book.spine[1:])

    def write_chapter(self, chapter_name, chapter_content):
        chapter = epub.EpubHtml(title=chapter_name, file_name=f"{chapter_name}.xhtml", lang="hr")
        chapter.content = chapter_content

        for image in os.listdir('./static'):
            if image in chapter.content:
                with open(f'./static/{image}', 'rb') as i:
                    content = i.read()
                    type = image.split('.')[-1]
                    img = epub.EpubImage(
                        uid = image.split('.')[0],
                        file_name = f'static/{image}',
                        media_type=f'image/{type}',
                        content=content
                    )
                    self.book.add_item(img)
        
        self.book.add_item(chapter)
        self.book.spine.append(chapter)


    def publish_book(self, title):
        self.add_toc()
        # add default NCX and Nav file
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        epub.write_epub(f"{title}.epub", self.book, {})
