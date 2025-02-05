# Directory Tracer

## Author: Justin Bornais

This is a simple Python program used for turning a given directory into a makeshift file server. It does this by tracingthrough  a directory and creating index.html webpages in each folder and subfolder, displaying the contents of each directory.

It also works for Github Pages. There is a sample workflow file [here](./.github/workflows/ghpages.yml] that runs the program and deploys it on Github Pages.
- **Note:** You may have to change it to use the `main` branch, or whichever branch you wish to deploy to GitHub Pages.
- It does not commit the index.html files to your branch directly. Instead, it runs the script and uploads it to the servers.

In order to run this code, you must have Python installed. Simply clone this repository into your directory. You may also update the `directoryScript.js` and `directoryStyles.css` files to change the styling.
- The CSS and JS code will be minimized by the program to ensure minimal HTML filesize. However, it will not properly remove single-line comments. So in JS, be sure to only use multi-line comments `/* */` if you wish to write comments.

Then, simply run `trace.py` by typing `python trace.py` or `py trace.py` and your webpages should be automatically created!

## Searching for Files and Folders
This program also incorporates [Fuse.js](https://www.fusejs.io/) for lightweight fuzzy-searching of files on the webpage.

## Omitting files and folders

To prevent files and folders from being included in the generated html pages, simply create a `.fileignore` file and list all file/folder names that you want omitted (one per line). By default, the `.fileignore` file is also ignored, so there's no need to add it to `.fileignore`.  
- **Note**: You do not need to include any `/` for folder names you want to omit. The name of the folder should suffice.
