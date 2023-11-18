
var Block = Quill.import('blots/block');
var InlineCode = Quill.import('blots/inline');
var BlockEmbed = Quill.import('blots/block/embed');

class InlineCodeBlot extends InlineCode {

    static blotName = 'inline-code'
    static tagName = 'code'
    static className = 'inline-code'
  

    constructor(quill, options) {
        super(quill, options)
        // Parse the toolbar configuration of the incoming module (that is, the two-dimensional array described earlier) and render the toolbar
    }

    static create(value) {
        const node = super.create(value)
        return node
    }
  
    static formats(node) {
        return node.textContent
    }  
    
}


class NoticeBlot extends Block{
    static blotName = 'notice'
    static tagName = 'div'
    static className = 'notice-block'

    constructor(quill, options) {
        super(quill, options)
        // Parse the toolbar configuration of the incoming module (that is, the two-dimensional array described earlier) and render the toolbar
    }

    static create(value) {
        const node = super.create(value)
        // node.setAttribute('contenteditable', true)
        node.classList.add('alert', 'alert-warning')
        node.innerHTML = '<pre><code></code></pre>'
        console.log("node: ", node, node.innerHTML, Object.keys(node), Object.values(node))
        return node
    }

    
}
   
  