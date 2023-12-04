/**
 * commonnly used functions
 */
let defaultToast = document.getElementById("error-toast")

window.addEventListener("load", () => {
    defaultToast = document.getElementById("error-toast")
})

/**
 * 
 * @param {HTMLElement} alert 
 */
function hideAlertError(alert){
    alert.classList.add("tw-hidden")
    alert.innerText = ""
}

/**
 * @param {HTMLElement} alert 
 * @param {string} text 
 */
function alertError(alert, text=""){
    alert.innerText = text
    alert.classList.remove("tw-hidden")
    alert.classList.remove("!tw-hidden")
}

/**
 * 
 * @param {HTMLElement | null} toast 
 * @param {"normal" | "danger"} text 
 */
function toastAlert(toast, text="", type="normal"){

    if (toast == null){
        toast = defaultToast
    }

    if (type === "danger"){
        toast.classList.add("bg-danger")
        toast.classList.remove("bg-primary")
    }else{
        toast.classList.remove("bg-danger")
        toast.classList.add("bg-primary")
    }

    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast)
    const toastBody = Array.from(toast.getElementsByClassName('toast-body'))
    toastBody.at(-1).innerText = text
    
    toastBootstrap.show()
}

/**
 * 
 * @param {HTMLElement} toast 
 * @param {string} text 
 */
function resetToast(toast){

    const toastBody = Array.from(toast.getElementsByClassName('toast-body'))
    toastBody.at(-1).innerText = ""

}

/**
 * @param {HTMLElement} btn 
 */
function disableBtn(btn){
    btn.disabled = true
}

/**
 * @param {HTMLElement} btn 
 */
function enableBtn(btn){
    btn.disabled = false
}

function isNameValid(text){
    const regex = /^[a-zA-Z0-9_-]+$/

    // Example usage
    return regex.test(text)
}


function isValidEmail(email){
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function isValidDomain(domain) {
    // Regular expression pattern to match a valid domain, including subdomains
    const domainPattern = /^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$/i;

    return domainPattern.test(domain);
}

function isValidUrl(url){

    try{
        new URL(url)
        return true
    }catch(e){
        return false
    }

}


function slugify(text) {
    if (text) {
        return text.toString().toLowerCase()
            .replace(/\s+/g, '-')           
            .replace(/[^\w-]+/g, '')        
            .replace(/--+/g, '-')           
            .replace(/^-+/, '')             
            .replace(/-+$/, '')
    }
    return '';
}

/**
 * 
 * @param {File} file 
 * @param {'MB'|'KB'} unit 
 * @returns 
 */
function getFileSize(file, unit='MB') {
    // Check if the input is a valid File object
    if (file instanceof File) {
        const fileSizeInBytes = file.size;

        if (unit === 'KB') {
            // Calculate the file size in kilobytes
            const fileSizeInKB = fileSizeInBytes / 1024;
            return fileSizeInKB.toFixed(2) // Round to 2 decimal places and add the unit
        } else if (unit === 'MB') {
            // Calculate the file size in megabytes
            const fileSizeInMB = fileSizeInBytes / (1024 * 1024);
            return fileSizeInMB.toFixed(2) // Round to 2 decimal places and add the unit
        }
    } else {
        return null; // Invalid input, return null
    }
}

function generateUUID() {
    let d = new Date().getTime();
    if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
      d += performance.now(); // Use high-precision timer if available
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = (d + Math.random() * 16) % 16 | 0;
      d = Math.floor(d / 16);
      return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
    });
}

/**
 * returns the current time + additional_time
 * @param {HTMLElement|null} datetimeElement 
 * @param {number} datetimeElement // used to add or subtract to the current time in ms
 */
function setDatetimeToLocal(datetimeElement, additonal_time=0){
    const currentDate = new Date();
    
    // Calculate the datetime 10 minutes from now
    const minDate = new Date(currentDate.getTime() + additonal_time);
    
    // Format the minDate as a string for the input field
    const minDateString = minDate.toISOString().slice(0, 16);
    // const minDateString = minDate.toUTCString();
    datetimeElement?.setAttribute('min', minDateString);

    return minDate
}

/**
 * 
 * @param {Date} datetime 
 * @returns 
 */
function toLocalTime(datetime){

    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        timeZoneName: 'short',
        hour12: true,
    };

    return datetime.toLocaleString('en-US', options);

}

/**
 * Makes the string input value format usable
 */
function UTCToUTCInputString(utcDateString){

    const utcDate = new Date(utcDateString)

    const year = utcDate.getUTCFullYear()
    const month = (utcDate.getUTCMonth() + 1).toString().padStart(2, '0')
    const day = utcDate.getUTCDate().toString().padStart(2, '0')
    const hours = utcDate.getUTCHours().toString().padStart(2, '0')
    const minutes = utcDate.getUTCMinutes().toString().padStart(2, '0')

    // Create a string in the format expected by the input element
    return `${year}-${month}-${day}T${hours}:${minutes}`

}  

function stringifyOnlyObjects(key, value) {
    if (typeof value === 'object' && value !== null) {
        return value; // Include only objects
    }
    return undefined; // Exclude all other types
}


/**
 * 
 * @param {Event} event 
 * @param {HTMLDivElement} contextMenu 
 * @returns 
 */
function setContextMenuPosition(event, contextMenu) {
    var mousePosition = {};
    var menuPosition = {};
    var menuDimension = {};

    menuDimension.x = contextMenu.offsetWidth;
    menuDimension.y = contextMenu.offsetHeight;
    mousePosition.x = event.pageX;
    mousePosition.y = event.pageY;


    function removeContextMenu(e){
        if (!contextMenu.contains(e.target) || e.key == "Escape") {
            contextMenu.classList.add("tw-hidden")
            document.removeEventListener("click", removeContextMenu)
            document.removeEventListener("keydown", removeContextMenu)
        }
    }
    
    // Hide context menu if clicked outside of it
    document.addEventListener("click", removeContextMenu)
    document.addEventListener("keydown", removeContextMenu)

    if (mousePosition.x + menuDimension.x > window.innerWidth + window.scrollX) {
        menuPosition.x = mousePosition.x - menuDimension.x;
    } else {
        menuPosition.x = mousePosition.x;
    }

    if (mousePosition.y + menuDimension.y > window.innerHeight + window.scrollY) {
        menuPosition.y = mousePosition.y - menuDimension.y;
    } else {
        menuPosition.y = mousePosition.y;
    }

    // Set the position of the context menu
    contextMenu.style.top = menuPosition.y + "px";
    contextMenu.style.left = menuPosition.x + "px";
    contextMenu.position = "fixed"
    // Make the context menu visible
    contextMenu.classList.remove("tw-hidden");

    return menuPosition;
}


function updateUrl(url){
    window.location = url
}

function isElementInViewport(el) {
    // tells  if the element is in the viewport
    var rect = el.getBoundingClientRect()
  
    return (
      rect.top >= -1 &&
      rect.left >= 0 &&
      rect.bottom <=
        (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    )
}



  /**
 * 
 * @param {string} text 
 * @param {"project"|"headings"} type 
 */
async function search(text, type){


    const res = await fetch(`/search/?${type}=${text}`, {
        method: "GET",
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
            // "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryABC123"
            }, 
    })

    let res_data = {}

    try {
        if (res.headers.get('content-type') === 'application/json') {
            res_data = await res.json();
            responseBody = JSON.stringify(data); // Store the JSON response body
        } else {
            res_data = await res.text();
            responseBody = data; // Store the text response body
        }
    } catch (e) {
        data = await res;
    }
    return [res.status, res_data]

}


let quickSearchData = []


/**
 * 
 * @param {{title: string, url: string}[]} data
 * 								
 * 							
 */
function setQuickSearchData(data){
	quickSearchData =  data
}

/**
 * 
 * @param {HTMLElement} editor 
 */
function getQuillHtml(editor){
    // remove span from code blocks
    
    let root = editor.root.cloneNode(true)

    root.querySelectorAll(".ql-code-block-container").forEach(ele => {
        const select = ele.querySelector('select')

        const divs = ele.querySelectorAll('.ql-code-block')
        
        if (select)
            ele.removeChild(select)

        let divContents = ``

        const spans = ele.querySelectorAll('span')

        spans.forEach(span => {
            const textNode = document.createTextNode(span.innerText) 
            span.innerHTML = ''
            span.replaceWith(textNode)
        })

        divs.forEach((div, index) => {

            div.removeAttribute("data-language")
            div.removeAttribute("data-highlighted")
            div.classList.remove("hljs")
            
            if (spans.length > 0) {
                divContents += `<div class="ql-code-block">${div.textContent}</div>\n`
            }else{
                divContents += `<div class="ql-code-block">${div.textContent}</div>`
            }

            
        })

        ele.innerHTML = divContents
    })

    return root.innerHTML
}