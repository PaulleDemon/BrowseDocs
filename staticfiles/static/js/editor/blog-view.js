
let headings = document.querySelectorAll("h1, h2, h3");
let tocContainer = document.getElementById("toc-container");
let tocElements = []

const tables = document.querySelectorAll('table')

tables.forEach((ele) => {

    const wrapperDiv = document.createElement('div')
    wrapperDiv.classList.add("tw-w-[100vw]", "tw-overflow-x-auto", "tw-flex", "tw-my-[2%]")

    ele.classList.add("table", "table-striped", "table-responsive", 
                        "table-bordered", "tw-w-full", 
                        "tw-max-w-[100vw]")

    const clonedTable = ele.cloneNode(true)
    wrapperDiv.appendChild(clonedTable)

    ele.parentNode.replaceChild(wrapperDiv, ele)

})

function generateTOC(){
    // generater table of contents

    let tocList = document.createElement("ul");
    tocElements = []
  // Iterate over the headings
    headings.forEach(function(heading) {
        let listItem = document.createElement("li")
        listItem.classList.add("tw-list-none", "tw-overflow-hidden", "tw-rounded-lg", "tw-flex", "tw-p-2")
        let link = document.createElement("a")
        link.classList.add( "tw-rounded-lg", "tw-w-[100%]")
        link.style.width = "100%"
        link.textContent = heading.textContent
        link.href = "#" + heading.id 

        listItem.appendChild(link)

        tocContainer.appendChild(listItem)
        tocElements.push(listItem)
    })

    let observer = new IntersectionObserver(highlightHandler, { threshold: 0.9 }) // Adjust the threshold as needed

    headings.forEach(function(heading) {
        observer.observe(heading)
    })

  tocContainer?.appendChild(tocList);

}

if (tocContainer)
    generateTOC()

function highlightHandler(entries){

    const allEntries = new Set(
        entries
        .filter((entry) => entry.isIntersecting == true)
        .map((entry) => entry.target)
    );

    let currentSection;

    for (let i = 0; i < headings.length; i++) {
        currentSection = headings[i]
        if (isElementInViewport(currentSection) || allEntries.has(currentSection)) {
            tocElements.forEach((link) => link.classList.remove("toc-active"))
            
            document
                .querySelector(`a[href="#${currentSection.id}"]`).parentNode
                .classList.add("toc-active");
            break
        }
    }
}



// }

// hljs.configure({languages:['python', 'javascript', 'java', 'rust', 
//                             'ruby', 'php', 'cpp', 'csharp', 'kotlin', 'json', 
//                             'html', 'css']})

document.querySelectorAll('.ql-code-block-container').forEach((el) => {
    const selectElement = el.querySelector("select");
    
    if (selectElement) {
        el.removeChild(selectElement);
    }

    hljs.highlightElement(el);
})

const codeBlocks = Array.from(document.querySelectorAll(".ql-code-block-container, pre"))


codeBlocks.forEach(ele => {
    const button = document.createElement('button')
    button.className = 'tw-p-4 btn copy-btn'
    button.setAttribute("title", "copy")
    button.setAttribute("data-bs-toggle", "tooltip")
    button.innerHTML = '<i class="bi bi-copy"></i>'
    button.onclick = () => copyCodeToClipboard(ele)
    ele.appendChild(button)

    ele.onscroll = () => {
        
        if (ele.scrollLeft > 10){
            button.style.display = "none"
        }else{
            button.style.display = "block"
        }

    }

})


function copyCodeToClipboard(element){

    navigator.clipboard.writeText(element.innerText).then(function() {
        toastAlert(null, "Copied to clipboard")

    }, function(err) {
        toastAlert(null, "Error copying", "danger")

    })
}


function addRawQueryParamToImageLinks() {
    // this is necessary to display images from githib
    const imgElements = document.querySelectorAll('img')

    imgElements.forEach(img => {
        const currentSrc = img.getAttribute('src')

        if (currentSrc && currentSrc.includes('?')) {
            img.setAttribute('src', `${currentSrc}&raw=true`)
        } else {
            img.setAttribute('src', `${currentSrc}?raw=true`)
        }
    })
}

addRawQueryParamToImageLinks()