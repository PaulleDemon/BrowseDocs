
let headings = document.querySelectorAll("h1, h2");
let tocContainer = document.getElementById("toc-container");
let tocElements = []


function generateTOC(){
    // generater table of contents

    let tocList = document.createElement("ul");
    tocElements = []
  // Iterate over the headings
    headings.forEach(function(heading) {
        let listItem = document.createElement("li")
        listItem.style.maxHeight = "min-fit"
        listItem.classList.add("tw-list-none", "tw-overflow-hidden", "tw-rounded-lg")
        let link = document.createElement("a")
        link.classList.add( "tw-rounded-lg", "tw-p-1", )
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
        currentSection = headings[i];
        if (isElementInViewport(currentSection) || allEntries.has(currentSection)) {
        tocElements.forEach((link) => link.classList.remove("tw-bg-gray-700", "tw-opacity-60", "tw-text-blue-400"));
        document
            .querySelector(`a[href="#${currentSection.id}"]`).parentNode
            .classList.add("tw-bg-gray-700", "tw-opacity-60", "tw-text-blue-400");
        break;
        }
    }
}

// function highLightCurrentIndex(e){
    
//     let scrollPosition = window.scrollY;

//     // tocContainer

//     headings.forEach(function(heading) {
//       let offsetTop = heading.offsetTop;
//       let offsetBottom = offsetTop + heading.clientHeight;

//       if (scrollPosition >= offsetTop && scrollPosition < offsetBottom) {
//         heading.classList.add("tw-bg-red-500")
//       } else {
//         heading.classList.remove("tw-bg-red-500")
//       }
//     })

// }

// window.addEventListener("scroll", highLightCurrentIndex)

document.querySelectorAll('pre, .ql-code-block-container').forEach((el) => {
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

