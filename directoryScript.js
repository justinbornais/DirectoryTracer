/* Check if on an Android device or not. */
var userAgent = navigator.userAgent.toLowerCase();
var Android = userAgent.indexOf("android") > -1;
var link = window.location.href;

const data = [];

const fuse = new Fuse(data, {
	keys: ['name'],
    includeScore: true
});

function getType(str) {
    let images = ['.bmp', '.ico', '.jpg', '.jpeg', '.jfif', '.png', '.svg', '.webp'];
    if(images.some(val => str.endsWith(val))) return "img";

    let videos = ['.mp4', '.webm', '.ogg', '.avi', '.mov', '.wmv', '.flv', '.mkv'];
    if(videos.some(val => str.endsWith(val))) return "video";
}

function addData(val) {
    var ul = document.getElementById("directory-list"); /* Get the ul element. */
    let data2 = [];
    
    if(val.length === 0) data2 = [...data];
    else {
        const results = fuse.search(val);
        data2 = results.map(result => {
            return {
                name: result.item.name,
                type: result.item.type
            };
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
            var elm = getType(object.name);
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