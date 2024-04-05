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
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
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
        .query { width: 100%; font-size: 20px; padding: 12px 20px; margin: 8px 0; box-sizing: border-box; }

        .container { display: flex; flex-wrap: wrap; }
        .col-1, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12 { box-sizing: border-box; }
        .col-1 { flex: 0 0 8.33%; max-width: 8.33%; }
        .col-2 { flex: 0 0 16.67%; max-width: 16.67%; }
        .col-3 {flex: 0 0 25%; max-width: 25%; }
        .col-4 {flex: 0 0 33.33%; max-width: 33.33%; }
        .col-5 {flex: 0 0 41.67%; max-width: 41.67%; }
        .col-6 {flex: 0 0 50%; max-width: 50%; }
        .col-7 {flex: 0 0 58.33%; max-width: 58.33%; }
        .col-8 {flex: 0 0 66.67%; max-width: 66.67%; }
        .col-9 {flex: 0 0 75%; max-width: 75%; }
        .col-10 {flex: 0 0 83.33%; max-width: 83.33%; }
        .col-11 {flex: 0 0 91.67%; max-width: 91.67%; }
        .col-12 {flex: 0 0 100%; max-width: 100%; }

        @media (min-width: 992px) {
            .col-lg-1, .col-lg-2, .col-lg-3, .col-lg-4, .col-lg-5, .col-lg-6, .col-lg-7, .col-lg-8, .col-lg-9, .col-lg-10, .col-lg-11, .col-lg-12 { box-sizing: border-box; }
            .col-lg-1 { flex: 0 0 8.33%; max-width: 8.33%; }
            .col-lg-2 { flex: 0 0 16.67%; max-width: 16.67%; }
            .col-lg-3 {flex: 0 0 25%; max-width: 25%; }
            .col-lg-4 {flex: 0 0 33.33%; max-width: 33.33%; }
            .col-lg-5 {flex: 0 0 41.67%; max-width: 41.67%; }
            .col-lg-6 {flex: 0 0 50%; max-width: 50%; }
            .col-lg-7 {flex: 0 0 58.33%; max-width: 58.33%; }
            .col-lg-8 {flex: 0 0 66.67%; max-width: 66.67%; }
            .col-lg-9 {flex: 0 0 75%; max-width: 75%; }
            .col-lg-10 {flex: 0 0 83.33%; max-width: 83.33%; }
            .col-lg-11 {flex: 0 0 91.67%; max-width: 91.67%; }
            .col-lg-12 {flex: 0 0 100%; max-width: 100%; }
        }

        @media (min-width: 1200px) {
            .col-xl-1, .col-xl-2, .col-xl-3, .col-xl-4, .col-xl-5, .col-xl-6, .col-xl-7, .col-xl-8, .col-xl-9, .col-xl-10, .col-xl-11, .col-xl-12 { box-sizing: border-box; }
            .col-xl-1 { flex: 0 0 8.33%; max-width: 8.33%; }
            .col-xl-2 { flex: 0 0 16.67%; max-width: 16.67%; }
            .col-xl-3 {flex: 0 0 25%; max-width: 25%; }
            .col-xl-4 {flex: 0 0 33.33%; max-width: 33.33%; }
            .col-xl-5 {flex: 0 0 41.67%; max-width: 41.67%; }
            .col-xl-6 {flex: 0 0 50%; max-width: 50%; }
            .col-xl-7 {flex: 0 0 58.33%; max-width: 58.33%; }
            .col-xl-8 {flex: 0 0 66.67%; max-width: 66.67%; }
            .col-xl-9 {flex: 0 0 75%; max-width: 75%; }
            .col-xl-10 {flex: 0 0 83.33%; max-width: 83.33%; }
            .col-xl-11 {flex: 0 0 91.67%; max-width: 91.67%; }
            .col-xl-12 {flex: 0 0 100%; max-width: 100%; }
        }

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
