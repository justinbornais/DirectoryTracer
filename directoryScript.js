/* Check if on an Android device or not. */
var userAgent = navigator.userAgent.toLowerCase();
var Android = userAgent.indexOf("android") > -1;
var link = window.location.href;

const fuse = new Fuse(d, {
	keys: ['n'],
    includeScore: true
});

const exts = {
    'doc': '📝',
    'docx': '📝',
    'exe': '💻',
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
    let d2 = [];
    
    if(val.length === 0) d2 = [...d];
    else {
        const results = fuse.search(val);
        d2 = results.map(result => {
            return {
                n: result.item.n,
                t: result.item.t
            };
        });
    }
    
    ul.textContent = "";

    let fh = d2.map(o => {
        if (o.t !== "d") return "";
        return `<li class="d"><a href="${o.n}">📁 ${o.n}</a></li>`;
    }).join('');
    ul.innerHTML += fh;
    
    var br = document.createElement("br");
    ul.appendChild(br);

    let ih = d2.map(o => {
        if (o.t !== "f") return "";
        let href = Android ? `https://docs.google.com/viewerng/viewer?url=${link}${o.n}`:`${o.n}`;
        return `<li class="f"><a href="${href}" target="_blank">${emoji(o.n)} ${o.n}</a></li>`;
    }).join('');
    ul.innerHTML += ih;
}

addData("");
document.getElementById("q").addEventListener("keyup", (e) => addData(e.target.value));
