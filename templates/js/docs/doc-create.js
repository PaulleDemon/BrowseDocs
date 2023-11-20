let repositories = document.getElementById("repositories")
const projectLogo = document.getElementById("project-logo")
const projectLogoInput = document.getElementById("project-logo-input")
const projectCreate = document.getElementById("create-project")

const docFiles = document.getElementById("doc-files")

const docAlert = document.getElementById("doc-create-alert")

const createProject = document.getElementById("create-project")


changeProjectIcon()

function disableImportBtns(disable=true){
    const docImportButton = Array.from(document.querySelectorAll("[name='import-repo']"))

    docImportButton.forEach(e => e.disabled = disable)
        
}


function showDocFiles(files=[]){

    let fileElements = ""

    files.forEach((e, i) => {
                                fileElements += ` 
                                                <div class="input-group">
                                                    <span class="input-group-text bi 
                                                            ${e.type=='folder'? 'bi-folder': 'bi-file-earmark-medical'}" 
                                                            style="border-radius:0px;"></span>
                                                    <div class="form-control">${e.path}</div>
                                                    
                                                    <span class="input-group-text" style="border-radius:0px;">
                                                        <input class="form-check-input" type="radio" name="docs" 
                                                            value="${e.path}" checked>
                                                    </span>
                                                </div>
                                            `     
                                console.log('foel elements: ', e.path)

                                }
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
        document.getElementById("repo-container").classList.add("tw-hidden")
        disableImportBtns(false)
        console.log("res data: ", res_data)
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
function configureProject(configuration={}){

    const docs = configuration.docs
    const config = configuration.config
    const project = configuration.project

    if (config.error){
        alertError(docAlert, config.error)
    }

    projectCreate.classList.remove('tw-hidden')

    if (docs)
        showDocFiles(docs)

    const fields = Array.from(createProject.querySelectorAll('[name]'))

    let field_name = ''

    const pgm_lang = createProject.querySelector("[id='pgm-lang']")
    const tool = createProject.querySelector("[id='tool']")

    let link_count = 0

    for (let x of fields){
        // extract configuration and fill in the fields
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
        }else if(field_name == 'name'){
            x.value = config['name'] || project

        }else if (config['social'] && ['reddit', 'stackoverflow', 'discord', 'twitter', 'mastodon'].includes(field_name.toLowerCase())){
            x.value = config['social'][field_name] || ''

        }else if(['link_name', 'link_url'].includes(field_name) && config['additional_links'] && Object.keys(config['additional_links']).length > link_count){
            
            if (field_name === 'link_name')
                x.value = Object.keys(config['additional_links'])[link_count]
            
            else if(field_name === 'link_url'){
                x.value = Object.values(config['additional_links'])[link_count]
                
                link_count += 1 // add only after link_url is updated
            }

        }
        else if(['opencollective', 'github', 'patreon', 'buymeacoffee'].includes(field_name) && config['sponsor']){
            x.value = config['sponsor'][field_name] || ''
        }
        else if (config[field_name]){ // this condition is necessary to ensure the csrf token is unaffected
            x.value = config[field_name] || ''
        }

        changeProjectIcon()

    }

    if (config['unique_name']){
        checkProjectNameAvailabilty(config['unique_name'])
    }

    
}

const uniqueProjectName = document.getElementById("unique-name")

const fetchController = new AbortController()
const fetchSignal = fetchController.signal

let projectNameTimeout = null

function checkProjectNameAvailabilty(name){


    if (projectNameTimeout){
        clearTimeout(projectNameTimeout)
    }

    projectNameTimeout = setTimeout(async () => {
            console.log("triggered")
            const res = await fetch("/docs/check-name-availability/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": Cookies.get('csrftoken'),
                    "Content-Type": "application/json"
                    }, 
                body: JSON.stringify({name: name}),
                // signal: fetchSignal
            })

            if (res.status == 200){
                data = await res.json()
                console.log("data: ", data, uniqueProjectName)
                if (data.exists === false){
                    uniqueProjectName.classList.remove("input-error")
                }else{
                    uniqueProjectName.classList.add("input-error")
                    toastAlert(null, "Unique name is already taken. Please choose another.", "danger")
                }
            }
        }
        , 100
    )

}


function validateFields(){

    const fields = Array.from(createProject.querySelectorAll('[name]'))

    for (let x of fields){

        let field_name = x.name
        if (field_name == 'unique_name' && (!isNameValid(x.value) || x.value.trim().length < 3)){
            toastAlert(null, `name can contain only alpha-numeric, _, -`, 'danger')
            return false
        }

        if (field_name == 'tags'){
            let tags = x.value.split(',')

            for(let x in tags){
                if(!isNameValid(x)){
                    toastAlert(null, `tags can contain only alpha-numeric, _, -`, 'danger')
                    return false
                }
            }
        }

        if (['version', 'name', 'about'].includes(field_name)){
            if (x.value.trim() === ''){
                toastAlert(null, `${field_name} cannot be empty`, 'danger')
                return false
            }
        }

        if (['project_logo', 'link_url', 'source_code'].includes(field_name)){

            if (x.value.trim() && !isValidUrl(x.value)){
                toastAlert(null, `Enter a valid ${field_name} url`, 'danger')
                return false
            }

        }

    }

    return true
}