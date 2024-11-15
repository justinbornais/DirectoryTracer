# Directory Tracer

## Author: Justin Bornais

This is a simple Python script used for tracing a directory and creating index.html webpages in each folder and subfolder, displaying the contents of each directory. This is beneficial for people who want to host a file server online, and it even works for GitHub Pages.

In order to run this code, you must have Python installed. Simply copy the `trace.py` file into your directory you want, or simply fork this repository. You do not have to edit the file whatsoever, as it will go by `os.curdir`.

Then, simply run `trace.py` by typing `python trace.py` or `py trace.py` and your webpages should be automatically created!

## Omitting files and folders

To prevent files and folders from being included in the generated html pages, simply create a `.fileignore` file and list all file/folder names that you want omitted (one per line). By default, the `.fileignore` file is also ignored, so there's no need to add it to `.fileignore`.  

Note: You do not need to include any `/` for folder names you want to omit. The name of the folder should suffice.
