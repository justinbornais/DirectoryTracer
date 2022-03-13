import os, sys
sys.setrecursionlimit(10000)

boilerplate1 = "<html>\n\n<head>\n</head>\n<body>\n    <ul>\n"
boilerplate2 = "    </ul>\n</body>\n</html>"

boilerplate1 = """<html>
<head>
    <style>
        .dir {
            font-size: 22px;
            color: blue;
        }
        .file {
            font-size: 18px;
        }
    </style>
</head>
<body>
    <ul>
"""

# tree -H . > index.html

def indexFolder(directory):
    folder_list = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))] # Source: https://www.codegrepper.com/code-examples/python/get+list+of+folders+in+directory+python
    if len(folder_list) > 0:
        
        for i in range(len(folder_list)):
            indexFolder(os.path.join(directory, folder_list[i]))

    file_list = [n for n in os.listdir(directory) if not n in folder_list] # My own list comprehension code!
    
    dir = directory.replace("\\", "/")[2:]
    
    f = open(directory + "\\index.html", "w")
    f.write(boilerplate1)
    
    # Write folder contents.
    f.write("        <li class=\"dir\"><b><a href=\"..\">..</a></b></li>\n")
    for i in range(len(folder_list)):
        f.write("        <li class=\"dir\"><b><a href=\"" + folder_list[i] + "\">" + folder_list[i] + "</a></b></li>\n")
    
    f.write("        <br />\n")
    
    # Write file contents.
    for i in range(len(file_list)):
        if file_list[i] != "index.html": f.write("        <li class=\"file\"><a href=\"" + file_list[i] + "\">" + file_list[i] + "</a></li>\n")
    
    f.write(boilerplate2)
    f.close()
    
indexFolder(os.curdir)
