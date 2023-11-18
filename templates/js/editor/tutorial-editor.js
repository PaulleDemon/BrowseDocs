const tags = document.getElementById("tags")
const draftBtn = document.getElementById("save-draft")
const publishButton = document.getElementById("publish")
const title = document.getElementById("tutorial-title")
const tutorial_id = document.getElementById("tutorial-id") 

editor.on('text-change', function(delta, oldDelta, source) {
    if (editor.getLength() > 250 && title.value.length > 10){
        publishButton.disabled = false
    }else{
        publishButton.disabled = true
    }

})



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

    console.log("ID: ", editor.getContents())

    data.append("id", id)
    data.append("title", heading)
    data.append("body", JSON.stringify({'delta': JSON.stringify(editor.getContents()), 'html': editor.root.innerHTML}))
    data.append("tag", tags.value)

    const res = await fetch(`/tutorial/save-draft/`, {
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
        tutorial_id.value = data.id
        toastAlert(null, "draft saved")
    }

}