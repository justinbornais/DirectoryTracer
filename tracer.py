import os, re, sys
sys.setrecursionlimit(10000)

def read_file_to_string(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()

    file_contents = re.sub(r'/\*.*?\*/', '', file_contents, flags=re.DOTALL)
    file_contents = ''.join(file_contents.splitlines())
    file_contents = file_contents.replace("\t", "").replace("  ", "")
    return file_contents

def split_path(path):
    parts = path.lstrip('./').split('/')
    return [part for part in parts if part]

title = "Directory Tracer"
css = read_file_to_string("./directoryStyles.css")
js = read_file_to_string("./directoryScript.js")

# getting ignored files and folders
ignored = ['.fileignore', 'directoryStyles.css', 'directoryScript.js']
if os.path.exists('.fileignore'):
    ignored = set(open('.fileignore', 'r').read().split('\n') + ignored)

# boilerplate used in the output html file
boilerplate = f"""<html>
<head>
    <title>{title}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <style>{css}</style>
</head>
<body>
    <div id="top"><h1>[parent]<a class="n" href="[base]">{title}</a>[dir]</h1>
        <input type="text" class="q" id="q" placeholder="Search for a file" />
    </div>
    <ul id="dl"></ul>
    <script src="https://cdn.jsdelivr.net/npm/fuse.js@6.6.2"></script>
<script>[data]{js}</script>\n</body>\n</html>"""

# recursive function that writes index.html and calls indexFolder for subdirectories
def indexFolder(directory, boilerplate, depth):
    print(f"Current directory: {directory}")

    bcopy = boilerplate
    base = "../" * depth
    boilerplate = boilerplate.replace("[base]", base)

    folder_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))] # Source: https://www.codegrepper.com/code-examples/python/get+list+of+folders+in+directory+python
    folder_list.sort()
    if len(folder_list) > 0:
        for i in range(len(folder_list)):
            if folder_list[i] not in ignored and not folder_list[i][0] == '.':
                indexFolder(os.path.join(directory, folder_list[i]), bcopy, depth + 1)

    file_list = [n for n in os.listdir(directory) if not n in folder_list] # anything not in folder_list is a file
    file_list.sort()
    jsData = ""
    
    # Add the folder path and a link to the parent page.
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
    boilerplate = boilerplate.replace('[dir]', title_string).replace('[parent]', parent_string)
    
    # Write folder contents.    
    for i in range(len(folder_list)):
        if folder_list[i] not in ignored and not folder_list[i][0] == '.':
            jsData += f'{{n:"{folder_list[i]}",t:"d"}},'

    # Write file contents.
    for i in range(len(file_list)):
        if file_list[i] not in ignored and file_list[i] != "index.html" and not file_list[i][0] == '.':
            jsData += f'{{n:"{file_list[i]}",t:"f"}},'
    
    boilerplate = boilerplate.replace("[data]", f"const d = [{jsData}];")
    
    # End off the html file.
    f = open(str(directory) + "/index.html", "w", encoding="utf8") # Create the file.
    f.write(boilerplate)
    f.close()

# Base case, where we index the current folder.
indexFolder(os.curdir, boilerplate, 0)
