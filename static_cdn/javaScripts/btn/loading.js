function SpinBorderRight(htmlElement) {
    let elm = htmlElement.innerText;
    htmlElement.innerHTML = elm + '<span class="spinner-border spinner-border-sm ms-2"></span> '
}

function spinnerGrowRight(htmlElement) {
    let elm = htmlElement.innerText;
    htmlElement.innerHTML = elm + '<span class="spinner-grow spinner-grow-sm ms-2 "></span>';
}

function spinnerGrowRightChangeText(text, htmlElement) {
    htmlElement.innerHTML = text +'<span class="spinner-grow spinner-grow-sm ms-2 "></span>';
}
function SpinBorderLeft(htmlElement) {
    let elm = htmlElement.innerText;
    htmlElement.innerHTML = '<span class="spinner-border spinner-border-sm ms-2"></span>' + elm;
}

function spinnerGrowLeft(htmlElement) {
    let elm = htmlElement.innerText;
    htmlElement.innerHTML ='<span class="spinner-grow spinner-grow-sm ms-2 "></span>' + elm
}

function spinnerGrowLeftChangeText(text, htmlElement) {
    let elm = htmlElement.innerText;
    htmlElement.innerHTML ='<span class="spinner-grow spinner-grow-sm ms-2 "></span>' + elm
}

function rotateElement(htmlElement) {
    let htmlElementChild = htmlElement.children[0];
    if (!htmlElementChild.classList.contains('fa-spin')) {
        htmlElementChild.classList.add('fa-spin');
    }
}

function stopRotation(htmlElement) {
    let htmlElementChild = htmlElement.children[0];
    if (htmlElementChild.classList.contains('fa-spin')){
        htmlElementChild.classList.remove('fa-spin');
    }
    else{
        htmlElement.innerHTML = htmlElement.innerText;
    }
}

function dynamicSpinner(htmlElement) {
    spinnerGrowRight(htmlElement)
}

function spinBack(htmlElement) {
    htmlElement.innerHTML = '<span class="fa fa-chevron-left me-2"></span><span class="spinner-border spinner-border-sm"></span>'
}