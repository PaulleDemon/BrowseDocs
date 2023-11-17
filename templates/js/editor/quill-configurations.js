const icons = window.Quill.import('ui/icons');

const tableContextMenu = document.getElementById("table-context-menu") 

let codeEditor = Array.from(document.querySelectorAll('.ql-editor pre'))

   

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
icons['table'] = '<i class="bi bi-table" id="insert-table"></i>'

icons['notice'] = '<i class="bi bi-exclamation-circle"></i>'
// icons['bettertable'] = '<i class="bi bi-table"></i>'

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
    [{ 'align': [] }],
    // ['clean'],                                        // remove formatting button
    // [{ 'size': fontSizeArr }],
    ['notice'],
    ['table'], // Add 'table' button
]
// Quill.register('modules/imageCompress', imageCompressor);

const Parchment = Quill.import('parchment')

Quill.register(NoticeBlot)
Quill.register(InlineCodeBlot)



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
    },
    theme: 'snow',
    placeholder: 'start writing....',
})

editor.on('text-change', function(delta, oldDelta, source) {
    if (source === 'user') {
        setTimeout(function() {
            hljs.highlightAll(); // Highlight code blocks after text change
        }, 0);

        // editor.updateContents(delta, 'api');
        // updateOutput();
    }
});
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
    const format = editor.getFormat(range)

   
    if (format['inline-code']) {
        // If inline code is already present, remove it
        editor.format( 'inline-code', false);
    } else {
        console.log("range: ", range.index + range.length, range.length)
        // If inline code is not present, insert it and add a space to the right
        editor.formatText(range.index, range.index + range.length, 'inline-code', true);
        editor.insertText(range.index + range.length + 2, ' ', true);
    }
    
}


const noticeButton = document.querySelector('.ql-notice')
// Handle the inline code button click
noticeButton.addEventListener('click', toggleNotice)


function toggleNotice() {
    console.log("notice toggle")

    const range = editor.getSelection();
    const format = editor.getFormat(range);
  
    // Toggle the 'yellow-background' format
    if (format['ql-notice']) {
        editor.formatText(range.index, range.index + range.length, 'ql-notice', false)
    } else {
        editor.formatText(range.index, range.index + range.length, 'ql-notice', true)
        // editor.format('notice', true)
    }
}

