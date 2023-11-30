const icons = window.Quill.import('ui/icons');
const tableContextMenu = document.getElementById("table-context-menu") 


const fontSizeArr = ['20px', '24px','32px','42px','54px','68px','84px','98px'];

var Size = Quill.import('attributors/style/size')
Size.whitelist = fontSizeArr
Quill.register(Size, true)

    
icons['bold'] = '<i class="bi bi-type-bold"></i>'
icons['italic'] = '<i class="bi bi-type-italic"></i>'
icons['underline'] = '<i class="bi bi-type-underline"></i>'
icons['strike'] = '<i class="bi bi-type-strikethrough"></i>'
icons['blockquote'] = '<i class="bi bi-quote"></i>'
icons['code-block'] = '<i class="bi bi-code-square"></i>'
icons['code-inline'] = '<i class="bi bi-code-slash"></i>'
icons['image'] = '<i class="bi bi-card-image"></i>'
icons['link'] = '<i class="bi bi-link"></i>'
icons['list']['ordered'] = '<i class="bi bi-list-ol"></i>'
icons['list']['bullet'] = '<i class="bi bi-list-ul"></i>'
icons['script']['sub'] = '<i class="bi bi-subscript"></i>'
icons['script']['super'] = '<i class="bi bi-superscript"></i>'
icons['indent']['-1'] = '<i class="bi bi-text-indent-right"></i>'
icons['indent']['+1'] = '<i class="bi bi-text-indent-left"></i>'
//icons['direction']['rtl'] = '<i class="bi bi-paragraph"></i>';
icons['align']['center'] = '<i class="bi bi-text-center"></i>'
icons['align']['justify'] = '<i class="bi bi-justify"></i>'
icons['align']['right'] = '<i class="bi bi-justify-right"></i>'
icons['align']['left'] = '<i class="bi bi-justify-left"></i>'
// icons['align'] = '<i class="bi bi-justify-left"></i>'
icons['table'] = '<i class="bi bi-table" id="insert-table"></i>'

icons['notice'] = '<i class="bi bi-exclamation-circle"></i>'

var toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
    ['code-block', 'code-inline'],
    ['blockquote', 'image', 'link'],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
    [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
    //[{ 'direction': 'rtl' }],                         // text direction
    //[{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
    [{ 'header': [1, 2, 3, false] }],
    // [{ 'align': [] }],
    [{ 'align': ['left', 'right', 'center', 'justify'] }],
    // ['clean'],                                        // remove formatting button
    // [{ 'size': fontSizeArr }],
    ['notice'],
    ['table'], // Add 'table' button
]
// Quill.register('modules/imageCompress', imageCompressor);

const Parchment = Quill.import('parchment')

Quill.register(NoticeBlot)
Quill.register(InlineCodeBlot)
Quill.register("modules/clipboard", PlainTextClipboard, true)
Quill.register("modules/imageCompressor", imageCompressor)
    

const Delta = Quill.import('delta')


let editor = new Quill('#editor', {
    modules: {
        syntax: {
            highlight: text => hljs.highlightAuto(text).value
        },
        table: true,  // disable table module
        toolbar: {
            container: toolbarOptions,
            handlers: {
                table: function(){
                    const table = editor.getModule('table')
                    table.insertTable(2, 2)
                    
                    Array.from(document.querySelectorAll(".ql-editor table")).forEach(e => {
                        e.addEventListener('contextmenu', (event) => {
                            event.preventDefault()
                            event.stopPropagation()
                            setContextMenuPosition(event, tableContextMenu)


                        })
                    })

                }
            }
        },
        imageCompressor: {
            quality: 0.6,
            maxWidth: 1000, // default
            maxHeight: 1000, // default
            imageType: 'image/png',
            ignoreImageTypes: ['image/gif']
        },
        clipboard: {
            matchers: [
                [Node.TEXT_NODE, (node, delta) => {
                    delta.ops = delta.ops.map(op => (typeof op.insert === 'string') ? { insert: op.insert.replace(/\n/g, ' ') } : op);
                    return new Delta().retain(delta.length(), { bold: false });
                  }]
            ]
        },
    },
    theme: 'snow',
    placeholder: 'start writing....',
})

editor.on('text-change', function(delta, oldDelta, source) {
    // console.log("source: ", editor.root)
    let selection = editor.getSelection();
    if (source === 'user') {
        setTimeout(function() {
            hljs.highlightAll(); // Highlight code blocks after text change
        }, 0);

        // editor.updateContents(delta, 'api');
        // updateOutput();
    }
    
    if (delta.ops && delta.ops.length > 0) {
        const lastOp = delta.ops[delta.ops.length - 1];
        if (lastOp.attributes && typeof lastOp.attributes === 'object' && 'code-block' in lastOp.attributes) {
            updateLanguage()
        }
    }

    function updateHeading() {
        // if current line is heading then update the heading with the id of the current title
        let cursorPosition = editor.getSelection()?.index;
        
        if (!cursorPosition)
            return
        
        let format = editor.getFormat(cursorPosition);
    
        if (format.header) {
            //if current line contains any heading formattig then add id
            const headingNodes = editor.root.querySelectorAll('h1, h2, h3');
            headingNodes.forEach(function (headingNode) {
                const headingText = headingNode.textContent.trim();
                
                const slugifiedId = slugify(headingText)
                headingNode.setAttribute('id', slugifiedId);
            })
        } 
    }

    updateHeading()

})


function updateLanguage(){
    document.querySelectorAll("div.ql-code-block-container")?.forEach(ele => {
        const select = ele.querySelector("select")

        ele.classList.forEach(className => {
            if (className.startsWith("language")){
                ele.classList.remove(className) // remove existing languages
            }
        })
        if (select.value)
            ele.classList.add(`language-${select.value}`)
        
        select.addEventListener("change", () => {
            ele.classList.forEach(className => {
                if (className.startsWith("language")){
                    ele.classList.remove(className) // remove existing languages
                }
            })
            ele.classList.add(`language-${select.value}`)
        })    

        
    })
}


// editor.on('selection-change', function(range, oldRange, source) {
    
// })

const table = editor.getModule('table')


function insertRowAbove(){
    table.insertRowAbove()
}

function insertRowBelow(){
    table.insertRowBelow()
}

function insertColumnRight(){
    table.insertColumnRight()
}

function insertColumnLeft(){
    table.insertColumnLeft()
}

function deleteRow(){
    table.deleteRow()
}

function deleteColumn(){
    table.deleteColumn()
}

function deleteTable(){
    table.deleteTable()
      
}


const inlineCodeButton = document.querySelector('.ql-code-inline')

// Handle the inline code button click
inlineCodeButton.addEventListener('click', toggleInlineCode)

// Function to toggle inline code format
function toggleInlineCode() {
    const range = editor.getSelection()
    const format = editor.getFormat(range.index, range.length)

    if (format['inline-code']) {
        editor.formatText(range.index, range.length, 'inline-code', false);
    } else {

        editor.formatText(range.index,  range.length, 'inline-code', true);
    }
    
}


const noticeButton = document.querySelector('.ql-notice')
// Handle the inline code button click
noticeButton.addEventListener('click', toggleNotice)


function toggleNotice() {

    const range = editor.getSelection();
    const format = editor.getFormat(range);
  
    if (format['ql-notice']) {
        editor.formatText(range.index, range.index + range.length, 'ql-notice', false)
    } else {
        // editor.formatText(range.index, range.index + range.length, 'ql-notice', true)
        editor.formatLine(range.index + 1, 1, 'ql-notice', true, Quill.sources.USER);
        
        // editor.format('notice', true)
    }
}


editor.keyboard.addBinding({
    key: 'Enter',
    collapsed: true,
    format: ['warning'],
  }, function(range, context) {
        editor.insertText(range.index, '\n', Quill.sources.USER);
        editor.setSelection(range.index + 1, Quill.sources.SILENT);
  })
