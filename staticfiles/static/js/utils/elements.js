

class TitleInput{

    /**
     * 
     * @param {HTMLTextAreaElement} element 
     */
    constructor(element){

        this.element = element
        
        this.disableEnter = this.disableEnter.bind(this)
        this.autoAdjustHeight = this.autoAdjustHeight.bind(this)

        element.addEventListener("keydown", this.disableEnter)
        element.addEventListener("change", this.autoAdjustHeight)
        element.addEventListener("input", this.autoAdjustHeight)
        // element.addEventListener("resize", () => setTimeout(this.autoAdjustHeight, 10))
        setTimeout(this.autoAdjustHeight, 10)

        window.addEventListener("resize", this.autoAdjustHeight)

    }

    disableEnter(e){
        if (e.key === 'Enter'){
            e.preventDefault()
        }
    }

    autoAdjustHeight() {
        console.log("YAA")
        this.element.style.height = 'auto'
        this.element.style.height = this.element.scrollHeight + 'px'
    }

}