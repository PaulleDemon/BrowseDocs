const searchListContainer = document.getElementById("search-list")
const projectListContainer = document.getElementById("project-list")


let searchTimeout = null

const PROJECT_CARD =  ({id, project_id, project_logo, unique_name, project_name, about, create_url, editable, source}) =>  `

                    <div class="tw-border-solid tw-border-[1px]
                            tw-rounded-lg tw-w-[60%] md:tw-max-w-[450px] tw-h-[200px] max-md:tw-w-[100%] 
                            tw-p-4 tw-flex  max-sm:tw-max-w-full tw-cursor-pointer
                            tw-shadow-xl
                            " 
                            onclick="updateUrl('/${project_id}')">

                        ${ project_logo ?
                            `<img src=${project_logo}
                                    class="tw-w-[50px] tw-h-[50px]"
                                    alt='' srcset=''>`
                            :
                            ''
                        }
                    
                        <div class="tw-ml-[4%] tw-flex tw-flex-col tw-w-full tw-overflow-x-hidden ${project_logo && 'tw-max-w-[80%]'}">

                            <div class="tw-text-xl tw-w-full">
                                ${project_name}
                            </div>
                            <div class="tw-mt-[2%] tw-text-sm tw-w-full subtext-color">
                                ${unique_name}
                            </div>
                            <div class="tw-mt-[2%] tw-max-h-[40%] tw-w-full tw-overflow-hidden subtext-color">
                                ${about}
                            </div>
                            ${ editable ?
                                `
                                <div class="tw-flex tw-justify-between tw-mt-auto">
                                    <a class="btn btn-success w-50 bi bi-pencil-square" href="${create_url}?step=2&repo_name=${source}&edit=${id}">
                                        Edit    
                                    </a>
                                    <button type="button" class="btn btn-primary bi bi-arrow-clockwise" onclick="updateDocument('${id}')">
                                            Update
                                    </button>
                                </div>
                                `
                                :
                                ''
                            }
                        </div>
                    </div>
                `

function searchProject(){
    // searchListContainer.
  
    const value = event.target.value.trim()

    if (searchTimeout){
        clearTimeout(searchTimeout)
    }

    if (value.length === 0){
        searchListContainer.classList.add("tw-hidden")
        projectListContainer.classList.remove("tw-hidden")
        return
    }

    searchTimeout = setTimeout(async () => {
        const [status, data] = await search(value, "project")

        if (status == 200){

            searchListContainer.classList.remove("tw-hidden")
            projectListContainer.classList.add("tw-hidden")
            
            searchListContainer.replaceChildren()

            data.forEach(i => {

                let source_path = new URL(i.source).pathname

                source_path = source_path.substring(1)

                searchListContainer.innerHTML += PROJECT_CARD({id: i.id, about: i.about, 
                                        editable: i.is_owner, project_logo: i.project_logo, 
                                        project_id:i.unique_id, source: source_path,
                                        unique_name: i.unique_name,
                                        project_name: i.name, create_url: "/project/create/"
                                    })
            })
            
        }

    }, 150)
        
}
