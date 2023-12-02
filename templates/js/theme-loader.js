/**
 * modifies theme
 */

const originalSetItem = localStorage.setItem
localStorage.setItem = function(key, value) {
    
    originalSetItem.apply(this, arguments)
    
    const event = new CustomEvent("storageChanged", {'detail': {'key': key}})
    window.dispatchEvent(event)
}

const darkHighlightJs = document.getElementById("highlightjs-dark")
const lightHighlightJs = document.getElementById("highlightjs-light")

const LIGHT_THEME = {
    '--text-color': '#000',
    '--background-color': '#fff',
    '--search-highlight-color': '#73ceff93',
    '--codeblock-bg': '#F6F8FA',
    '--toc-highlight-bg': '#a5a5a5a4'

}

const DARK_THEME = {
    '--text-color': '#fff',
    '--background-color': '#0F172A',
    '--search-highlight-color': '#73ceff93',
    '--codeblock-bg': '#080e1c',
    '--toc-highlight-bg':'#20306857',
}

window.addEventListener("load", () => {
    if (localStorage.getItem("theme") === null){
        setTheme(false)
    }
    updateTheme()
})

const root_style = document.documentElement.style

function modifyTheme(theme=LIGHT_THEME){
    for (let x of Object.entries(theme)){
        root_style.setProperty(x[0], x[1])
    }

}

function updateTheme(){
    if (localStorage.getItem("theme") == '0'){
        modifyTheme(DARK_THEME)
        darkHighlightJs.removeAttribute('disabled')
        lightHighlightJs.setAttribute('disabled', 'true')
        document.querySelector('body').setAttribute("data-bs-theme", "dark")

    }else{
        modifyTheme(LIGHT_THEME)
        lightHighlightJs.removeAttribute('disabled')
        darkHighlightJs.setAttribute('disabled', 'true')
        document.querySelector('body').setAttribute("data-bs-theme", "light")

    }

}

function setTheme(dark=false){

    if (dark){
        localStorage.setItem("theme", '1')
    }else{
        localStorage.setItem("theme", '0')
        console.log("light")
    }

}

function toggleTheme(){
    if (localStorage.getItem("theme") === '0'){
        setTheme(true)
    }else{
        setTheme(false)
    }
}


window.addEventListener("storageChanged", updateTheme, false)
