function getDate() {
    return document.getElementById('dateSearch').value;
}

async function call() {
    let request = '';
    request = 'https://api.nasa.gov/planetary/apod?date=' + getDate() + '&api_key=GXacxntSzk6wpkUmDVw4L1Gfgt4kF6PzZrmSNWBb';
    let response = await fetch(request);
    let data = await response.json();
    p = document.getElementById("description");
    p.innerHTML = data.explanation;

    img = document.getElementById("spacePic");
    img.src = data.url;
}