import os, re, sys
sys.setrecursionlimit(10000)

def read_file_to_string(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()

    file_contents = re.sub(r'/\*.*?\*/', '', file_contents, flags=re.DOTALL)
    file_contents = ''.join(file_contents.splitlines())
    file_contents = file_contents.replace("\t", "").replace("  ", "")
    if file_path.endswith(".css"):
        file_contents = file_contents.replace(" ", "")
    return file_contents

css = read_file_to_string("./directoryStyles.css")
js = read_file_to_string("./directoryScript.js")

# getting ignored files and folders
ignored = ['.fileignore', 'directoryStyles.css', 'directoryScript.js']
if os.path.exists('.fileignore'):
    ignored = set(open('.fileignore', 'r').read().split('\n') + ignored)

# boilerplate used in the output html file
boilerplate1 = f"""<html>
<head>
    <title>Site Title</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <style>{css}</style>
</head>
<body>
    <h2>View Directory Contents</h2>
    <div class="i"><input type="text" class="q" id="q" placeholder="Search for a file" /></div>
    """

boilerplate2 = f"""    </ul>
    <script src="https://cdn.jsdelivr.net/npm/fuse.js@6.6.2"></script>
    <script>{js}</script>\n</body>\n</html>"""

# recursive function that writes index.html and calls indexFolder for subdirectories
def indexFolder(directory):
    print(f"Current directory: {directory}")
    folder_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))] # Source: https://www.codegrepper.com/code-examples/python/get+list+of+folders+in+directory+python
    folder_list.sort()
    if len(folder_list) > 0:
        for i in range(len(folder_list)):
            if folder_list[i] not in ignored and not folder_list[i][0] == '.':
                indexFolder(os.path.join(directory, folder_list[i]))

    file_list = [n for n in os.listdir(directory) if not n in folder_list] # anything not in folder_list is a file
    file_list.sort()
    jsData = ""

    f = open(str(directory) + "/index.html", "w", encoding="utf8") # Create the file.
    
    # Fill with initial HTML code.
    f.write(boilerplate1)
    if directory != ".":
        f.write("   <h1>" + directory.replace("\\", "/") + "</h1>\n")
        f.write("        <li class=\"d\"><b><a href=\"..\">⬆ Parent</a></b></li></br>\n")
        
    f.write("    <ul id=\"dl\">\n")
    
    # Write folder contents.    
    for i in range(len(folder_list)):
        if folder_list[i] not in ignored and not folder_list[i][0] == '.':
            jsData += f'{{n:"{folder_list[i]}",t:"d"}},'

    # Separate folders from files.
    f.write("        <br />\n")

    # Write file contents.
    for i in range(len(file_list)):
        if file_list[i] not in ignored and file_list[i] != "index.html" and not file_list[i][0] == '.':
            jsData += f'{{n:"{file_list[i]}",t:"f"}},'
    
    boilerplate3 = boilerplate2.replace("const data = [];", f"const data = [{jsData}];")
    
    # End off the html file.
    f.write(boilerplate3)
    f.close()

# Base case, where we index the current folder.
indexFolder(os.curdir)
