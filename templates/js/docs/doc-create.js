let repositories = document.getElementById("repositories")
const projectLogo = document.getElementById("project-logo")
const projectLogoInput = document.getElementById("project-logo-input")
const projectCreate = document.getElementById("create-project")

const docFiles = document.getElementById("doc-files")

const createProject = document.getElementById("create-project")


function disableImportBtns(disable=true){
    const docImportButton = Array.from(document.querySelectorAll("[name='import-repo']"))

    docImportButton.forEach(e => e.disabled = disable)
        
}


function showDocFiles(files=[]){

    const fileElements = ""

    fileElements += files.forEach((e, i) => (` <div class="input-group">
                                                    <span class="input-group-text bi 
                                                            ${e.type=='file'? 'bi-file-earmark-medical': 'bi-folder'}" 
                                                            style="border-radius:0px;"></span>
                                                    <input type="text" class="form-control" disabled value="Readme">
                                                    <span class="input-group-text" style="border-radius:0px;">
                                                        <input class="form-check-input" type="radio" name="docs" 
                                                            value="${e.name}" >
                                                    </span>
                                                </div>
                                            `
                                            )
                                        )

    docFiles.innerHTML = fileElements

}


async function importRepository(repo){
    
    disableImportBtns(true)

    data = {
        'repo': repo // format owner/reponame
    }

    const res = await fetch("/repo/import/", {
        method: "POST",
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
            "Content-Type": "application/json"
            // "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryABC123"
            }, 
        body: JSON.stringify(data)
    })

    let res_data = {}

    try {
        if (res.headers.get('content-type') === 'application/json') {
            res_data = await res.json();
            responseBody = JSON.stringify(data); // Store the JSON response body
            
            console.log("response body: ", responseBody)

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

        if (res_data.error){
            toastAlert(null, res_data.error, "danger")
        }
        else if (res_data.repo){
            toastAlert(null, res_data.repo, "danger")
        }
      
    }

    if (res.status == 404){
        if (res_data){
            toastAlert(null, "Repository not found", "danger")
        }
      
    }

    if (res.status == 200){
        repositories.classList.add("!tw-hidden")
        configureProject(res_data)
    }

    if (res.status == 429){
        toastAlert(null, "Too many requests please wait")
    }

    if (res.staus == 302){
        window.location = res.redirect
    }
    
    disableImportBtns(false)

}


function changeProjectIcon(){

    if (!isValidUrl(projectLogoInput.value)){
        projectLogo.src = " "
    }
    else{
        projectLogo.src = projectLogoInput.value
    }
}

/**
 * 
 * @param {} config // files contents of .browsedocs.json
 */
function configureProject(config={}){

    const fields = Array.from(createProject.querySelectorAll('[name]'))

    let field_name = ''

    const pgm_lang = fields.getElementById('pgm-lang')
    const tool = fields.getElementById('tool')




    for (let x of fields){
        field_name = x.name
       
        if (field_name === 'doc-type' && config['doc-type']){
            if (config['doc-type'] == 'pgm-lang'){
                pgm_lang.selected = true
                tool.selected = false
            }
            else{
                tool.selected = true
                pgm_lang.selected = false
            }
        }else if (field_name==''){

        }else{
            x.value = config[field_name] || ''
        }

    }

    
}