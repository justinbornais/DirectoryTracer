/* Check if on an Android device or not. */
var userAgent = navigator.userAgent.toLowerCase();
var Android = userAgent.indexOf("android") > -1;
var link = window.location.href;

const data = [];

const fuse = new Fuse(data, {
	keys: ['n'],
    includeScore: true
});

const exts = {
    'doc': '📝',
    'docx': '📝',
    'csv': '📊',
    'xls': '📊',
    'xlsx': '📊',
    'jpg': '📷',
    'jpeg': '📷',
    'png': '📷',
    'pdf': '📄'
};
  
const emoji = (f) => {
    const ext = f.split('.').pop();
    return exts[ext] || '📄';
};

function addData(val) {
    var ul = document.getElementById("dl"); /* Get the ul element. */
    let data2 = [];
    
    if(val.length === 0) data2 = [...data];
    else {
        const results = fuse.search(val);
        data2 = results.map(result => {
            return {
                n: result.item.n,
                t: result.item.t
            };
        });
    }
    
    ul.textContent = "";
    
    data2.map(object => {
        if(object.t === "d") {
            var a = document.createElement("a");
            a.href = `${object.n}`;
            a.value = `📁 ${object.n}/`;
            a.innerHTML = `📁 ${object.n}/`;
            var li = document.createElement("li");
            li.setAttribute("class", "d");
            li.appendChild(a);
            ul.appendChild(li);
        }
    });
    
    var br = document.createElement("br");
    ul.appendChild(br);
    
    data2.map(object => {
        if(object.t === "f") {
            let em = emoji(object.n);
            var a = document.createElement("a");
            if(Android) a.href = `https://docs.google.com/viewerng/viewer?url=${link}${object.n}`;
            else a.href = `${object.n}`;
            a.target = "_blank";
            a.value = `${em} ${object.n}`;
            a.innerHTML = `${em} ${object.n}`;
            var li = document.createElement("li");
            li.setAttribute("class", "f");
            li.appendChild(a);
            ul.appendChild(li);
        }
    });
}

addData("");

document.getElementById("q").addEventListener("keyup", (e) => addData(e.target.value));