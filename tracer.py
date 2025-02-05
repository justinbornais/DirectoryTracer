import os, re, sys
sys.setrecursionlimit(10000) # Prevents program failure if recursion is too deep.

# Reads file as string.
# It also removes as much whitespace as psosible, as well as comments.
def read_file_to_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    file_contents = re.sub(r'/\*.*?\*/', '', file_contents, flags=re.DOTALL)
    file_contents = ''.join(file_contents.splitlines())
    file_contents = file_contents.replace("\t", "").replace("  ", "")
    return file_contents

# Get each section of a path.
def split_path(path):
    parts = path.lstrip('./').split('/')
    return [part for part in parts if part]

## Defined constants.
TITLE = "Directory Tracer"

css = read_file_to_string("./directoryStyles.css")
js = read_file_to_string("./directoryScript.js")

# Getting ignored files and folders.
ignored = ['.fileignore', 'directoryStyles.css', 'directoryScript.js']
if os.path.exists('.fileignore'):
    ignored = set(open('.fileignore', 'r').read().split('\n') + ignored)

# Boilerplate used in the output HTML file.
boilerplate = f"""<html>
<head>
    <title>{TITLE}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <style>{css}</style>
</head>
<body>
    <div id="top"><h1>[parent]<a class="n" href="[base]">{TITLE}</a>[dir]</h1>
        <input type="text" class="q" id="q" placeholder="Search for a file" />
    </div>
    <ul id="dl"></ul>
    <script src="https://cdn.jsdelivr.net/npm/fuse.js@6.6.2"></script>
<script>[data]{js}</script>\n</body>\n</html>"""

# Adds the folder path and a link to the parent page.
def writeFolderName(directory, boilerplate):
    title_string = ""
    parent_string = ""
    if directory != ".":
        dir_string = directory.replace("\\", "/")
        parts = split_path(dir_string)
        title_string = " - "
        for i in range(len(parts)):
            depth = "../" * (len(parts) - i)
            title_string += f"<a class=\"n\" href=\"{depth}{parts[i]}\">{parts[i]}</a>"
            if i != len(parts) - 1: title_string += "/"
       
        parent_string = '<b><a href=".." class="p">←</a></b>'
    
    return boilerplate.replace('[dir]', title_string).replace('[parent]', parent_string)

# Writes folder contents in JSON format.
def writeFolderJSON(folder_list):
    data = ""
    for i in range(len(folder_list)):
        if folder_list[i] not in ignored and not folder_list[i][0] == '.':
            data += f'{{n:"{folder_list[i]}",t:"d"}},'
    return data

def writeFileJSON(file_list):
    data = ""
    for i in range(len(file_list)):
        if file_list[i] not in ignored and file_list[i] != "index.html" and not file_list[i][0] == '.':
            data += f'{{n:"{file_list[i]}",t:"f"}},'
    return data

# Recursive function that writes index.html and calls indexFolder for subdirectories.
def indexFolder(directory, boilerplate, depth):
    print(f"Current directory: {directory}")

    bcopy = boilerplate
    base = "../" * depth
    boilerplate = boilerplate.replace("[base]", base)

    folder_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))] # Get all folders in the current directory.
    folder_list.sort()
    if len(folder_list) > 0:
        for i in range(len(folder_list)):
            if folder_list[i] not in ignored and not folder_list[i][0] == '.':
                indexFolder(os.path.join(directory, folder_list[i]), bcopy, depth + 1) # Run function recursively on all valid subfolders.

    file_list = [n for n in os.listdir(directory) if not n in folder_list] # Anything not in folder_list is a file.
    file_list.sort()
    jsData = ""
    
    # Add the folder path and a link to the parent page.
    boilerplate = writeFolderName(directory, boilerplate)
    jsData += writeFolderJSON(folder_list)
    jsData += writeFileJSON(file_list)
    boilerplate = boilerplate.replace("[data]", f"const d = [{jsData}];")
    
    # Write the html file.
    f = open(str(directory) + "/index.html", "w", encoding="utf8") # Create the file.
    f.write(boilerplate)
    f.close()

# Base case, where we index the current folder.
indexFolder(os.curdir, boilerplate, 0)
