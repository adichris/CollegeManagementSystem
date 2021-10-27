function SpinBorderRight(htmlElement) {
    let elm = htmlElement.innerText;
    htmlElement.innerHTML = elm + '<span class="spinner-border spinner-border-sm ms-2"></span> '
}

function spinnerGrowRight(htmlElement) {
    let elm = htmlElement.innerText;
    htmlElement.innerHTML = elm + '<span class="spinner-grow spinner-grow-sm ms-2 "></span>'
}

function rotateElement(htmlElement) {
    let htmlElementChild = htmlElement.children[0];
    if (!htmlElementChild.classList.contains('fa-spin')) {
        htmlElementChild.classList.add('fa-spin');
    }
}

function stopRotation(htmlElement) {
    if (htmlElement.classList.contains('fa-spin')){
        htmlElement.classList.remove('fa-spin');
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