docImportButton = document.getElementById("") 
repositories = document.getElementById("repositories")


async function importRepository(repo){
    const res = await fetch("/repo/import/", {
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
        if (res_data.json){
            toastAlert(null, "", "danger")
        }
      
    }

    if (res.status == 200){
        toastAlert(null, "")
    }

    if (res.status == 429){
        toastAlert(null, "Too many requests please wait")
    }

    if (res.staus == 302){
        window.location = res.redirect
    }
    
    testMailBtn.disabled = false
    testMailBtn.classList.remove("spinner-border", "text-light")
}