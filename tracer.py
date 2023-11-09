import os, sys
sys.setrecursionlimit(10000)

# getting ignored files and folders
ignored = ['.fileignore']
if os.path.exists('.fileignore'):
    ignored = set(open('.fileignore', 'r').read().split('\n') + ['.fileignore'])

# boilerplate used in the output html file
boilerplate1 = """<html>
<head>
    <title>Site Title</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <style>
        body { margin: 2rem; font-family: sans-serif; }
        @media (prefers-color-scheme: light) {
            a, a:visited { color: blue; }
            a:hover { background-color: yellow; }
        }
        @media (prefers-color-scheme: dark) {
            body { background-color: #121212; color: #f5f5f5; }
            a, a:visited { color: skyblue; }
            a:hover { color: white; }
        }
        ul, li { list-style-type: none; }
        .dir { font-size: 20px; font-weight: bold; }
        .file { font-size: 18px; }
        .input { padding-right: 10%; }
        .query { width: 100%; font-size: 20px; padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box; }
    </style>
</head>
<body>
    <h2>View Directory Contents</h2>
    <div class="input"><input type="text" class="query" id="query" class="query" placeholder="Search for a file" /></div>
    """

boilerplate2 = "    </ul>\n</body>\n</html>"
boilerplate2 = """    </ul>
    <script src="https://cdn.jsdelivr.net/npm/fuse.js@6.6.2"></script>
    <script>
        
        // Check if on an Android device or not.
        var userAgent = navigator.userAgent.toLowerCase();
        var Android = userAgent.indexOf("android") > -1;
        var link = window.location.href;
        
        const data = [];
        
        const fuse = new Fuse(data, {
            keys: ['name'],
            includeScore: true
        })
        
        function addData(val) {
            var ul = document.getElementById("directory-list"); // Get the ul element.
            let data2 = [];
            
            if(val.length === 0) data2 = [...data];
            else {
                const results = fuse.search(val);
                data2 = results.map(result => {
                    return {
                        name: result.item.name,
                        type: result.item.type
                    }
                });
            }
            
            ul.textContent = "";
            
            data2.map(object => {
                if(object.type === "folder") {
                    var a = document.createElement("a");
                    a.href = `${object.name}`;
                    a.value = `📁 ${object.name}/`;
                    a.innerHTML = `📁 ${object.name}/`;
                    var li = document.createElement("li");
                    li.setAttribute("class", "dir");
                    li.appendChild(a);
                    ul.appendChild(li);
                }
            });
            
            var br = document.createElement("br");
            ul.appendChild(br);
            
            data2.map(object => {
                if(object.type === "file") {
                    var a = document.createElement("a");
                    if(Android) a.href = `https://docs.google.com/viewerng/viewer?url=${link}${object.name}`;
                    else a.href = `${object.name}`;
                    a.target = "_blank";
                    a.value = `📄 ${object.name}`;
                    a.innerHTML = `📄 ${object.name}`;
                    var li = document.createElement("li");
                    li.setAttribute("class", "file");
                    li.appendChild(a);
                    ul.appendChild(li);
                }
            });
        }
        
        addData("");
        
        document.getElementById("query").addEventListener("keyup", (e) => addData(e.target.value));
        
    </script>\n</body>\n</html>"""

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
    jsData = "";

    f = open(str(directory) + "/index.html", "w", encoding="utf8") # Create the file.
    
    # Fill with initial HTML code.
    f.write(boilerplate1)
    if directory != ".":
        f.write("   <h1>" + directory.replace("\\", "/") + "</h1>\n")
        f.write("        <li class=\"dir\"><b><a href=\"..\">⬆ Parent</a></b></li></br>\n")
        
    f.write("    <ul id=\"directory-list\">\n")
    
    # Write folder contents.    
    for i in range(len(folder_list)):
        if folder_list[i] not in ignored and not folder_list[i][0] == '.':
            jsData += f'{{name: "{folder_list[i]}", type: "folder"}},'

    # Separate folders from files.
    f.write("        <br />\n")

    # Write file contents.
    for i in range(len(file_list)):
        if file_list[i] not in ignored and file_list[i] != "index.html" and not file_list[i][0] == '.':
            jsData += f'{{name: "{file_list[i]}", type: "file"}},'
    
    boilerplate3 = boilerplate2.replace("const data = [];", f"const data = [{jsData}]")
    
    # End off the html file.
    f.write(boilerplate3)
    f.close()

# Base case, where we index the current folder.
indexFolder(os.curdir)
