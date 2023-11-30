/**
 * 
 * @param {*} projectid 
 * @param {*} btn 
 * @returns 
 */
async function updateDocument(projectid){
    event?.stopPropagation()
    event?.preventDefault()

    if (event)
        event.target.disabled = true

    const res = await fetch(`/doc/update/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({projectid})
    })

    let data = undefined
    try {
        if (res.headers.get('content-type') === 'application/json') {
            data = await res.json();
            responseBody = JSON.stringify(data); // Store the JSON response body
        } else {
            data = await res.text();
            responseBody = data; // Store the text response body
        }
    } catch (e) {
        data = await res;
        return
    }

    if (res.status == 400){

        if (res_data.error){
            toastAlert(null, `Error updating document ${res_data.error}`, "danger")
        }
    }
    else if (res.status == 200){

        toastAlert(null, "Document is updating please wait.")
        return
    }
    
    else{
        toastAlert(null, "Error updating document. Try again later.")
    }

    if (event)
        event.target.disabled = false
    
}
