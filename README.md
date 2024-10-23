# Wind and Truth Ebooker
This simple project generates a ".epub" file that is compatible with ebook readers.

Currently, this will only work with the weekly releases of "Wind and Truth" by Brandon Sanderson on the [Reactormag website](https://reactormag.com/columns/wind-and-truth/)

## Description
This project uses selenium library to render the website content in a headless mode and extracts the html from each chapter. It also uses the ebooker library to take the extracted html and generate a compatible ".epub" file.

This project also includes a caching mechanism so that only the new content is downloaded on successive runs.

## Setup
1. `python -m venv venv`
2. `python -m pip install -r requirements`

## Generating the book
Simply run `python main.py` from the virtual environment.

## Adding new chapters
Simply append the url of the new chapters to the `chapters` array in `main.py`.
