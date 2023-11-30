const searchListContainer = document.getElementById("search-list")
const projectListContainer = document.getElementById("project-list")


let searchTimeout = null

const PROJECT_CARD =  ({id, project_id, project_logo, unique_name, project_name, about, create_url, editable, source}) =>  `

                    <div class="tw-border-solid tw-border-[1px] tw-bg-gray-800
                            tw-rounded-lg tw-w-[60%] md:tw-max-w-[450px] tw-h-[200px] max-md:tw-w-[100%] 
                            tw-p-4 tw-flex  max-sm:tw-max-w-full tw-cursor-pointer
                            " 
                            onclick="updateUrl({% url "get-docs" unique_id=${project_id} %})">

                        ${ project_logo ?
                            `<img src=${project_logo}
                                    class="tw-w-[50px] tw-h-[50px]"
                                    alt='' srcset=''>`
                            :
                            ''
                        }
                    
                        <div class="tw-ml-[4%] tw-flex tw-flex-col tw-max-w-[80%] tw-overflow-x-hidden">
                            <div class="tw-text-xl tw-w-full">
                                ${project_name}
                            </div>
                            <div class="tw-mt-[2%] tw-text-sm tw-w-full tw-text-gray-400">
                                ${unique_name}
                            </div>
                            <div class="tw-mt-[2%] tw-max-h-[40%] tw-w-full tw-overflow-hidden tw-text-gray-400">
                                ${about}
                            </div>
                            ${ editable &&
                                `<a class="btn btn-success bi bi-pencil-square tw-m-1" href="${create_url}?step=2&repo_name=${source}&edit=${id}">
                                    Edit    
                                </a>`
                            }
                        </div>
                    </div>
                `

function searchProject(){
    // searchListContainer.
  
    const value = event.target.value.trim()


    if (value.length == 0){
        searchListContainer.classList.add("tw-hidden")
        projectListContainer.classList.remove("tw-hidden")
        return
    }

    if (searchTimeout){
        clearTimeout(searchTimeout)
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
