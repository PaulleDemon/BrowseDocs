const tags = document.getElementById("tags")
const draftBtn = document.getElementById("save-draft")
const publishButton = document.getElementById("publish")
const title = document.getElementById("tutorial-title")
const tutorial_id = document.getElementById("tutorial-id") 
const tutorialCreateContainer = document.getElementById("tutorial-editor")

const projectId = document.getElementById("project_id")


const quillEditorTextArea = document.getElementById("quill-textarea")


const titleInput = new TitleInput(title)

const body_data = JSON.parse(document.getElementById('body-data').textContent)

const params = new URLSearchParams(window.location.search)

const project_id = params.get("project_id")
if (project_id){
    projectId.value = project_id
}

if (body_data){
   
    setTimeout(() => editor.setContents(
            JSON.parse(body_data)
        ), 100)
}

setTimeout(updateLanguage, 100)

if (editor.getLength() > 250 && title.value.length > 10){
    publishButton.disabled = false
}else{
    publishButton.disabled = true
}

editor.on('text-change', function(delta, oldDelta, source) {
    if (editor.getLength() > 250 && title.value.length > 10){
        publishButton.disabled = false
    }else{
        publishButton.disabled = true
    }

})

tutorialCreateContainer.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault()
  
        saveDraft()
      }
})


function onSubmit(){

    const heading = title.value


    if (heading.length < 10){
        toastAlert(null, "Please add a proper title", "danger")
        return false
    }

    if (editor.getLength() < 200){
        toastAlert(null, "Sorry tutorials that are too short(undeer 200 characters) aren't allowed to publish", "danger")
        return false
    }

    quillEditorTextArea.value = JSON.stringify({'delta': JSON.stringify(editor.getContents()), 'html': editor.root.innerHTML})

    return true

}


async function saveDraft(){

    const id = tutorial_id.value || ''
    const heading = title.value

    if (heading.length < 10){
        toastAlert(null, "Please add a proper title", "danger")
        return 
    }

    if (editor.getLength() < 30){
        toastAlert(null, "Please add atleast 30 characters to save as draft", "danger")
        return
    }

    let data = new FormData()

    data.append("id", id)
    data.append("title", heading)
    data.append("body", JSON.stringify({'delta': JSON.stringify(editor.getContents()), 'html': editor.root.innerHTML}))
    data.append("tag", tags.value)
    data.append("project", projectId.value)

    const res = await fetch(`/tutorial/save-draft/?edit=${id}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
            // "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryABC123"
            }, 
        body: data
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
        console.log("response: ", res);
        data = await res;
        return
    }

    if (res.status == 400){
        toastAlert(null, "Invalid data", "danger")
    }else if (res.status == 200){

        tutorial_id.value = res_data.id

        const urlParams = new URLSearchParams(window.location.search)
        urlParams.set('edit', res_data.id)

        history.pushState(null, null, '?' + urlParams.toString());
        toastAlert(null, "draft saved")
    }

}
