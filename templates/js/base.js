// initialization

// const defaultToast = document.getElementById("error-toast")

const navSearch = document.getElementById("nav-search")

const quickSearchContainer = document.getElementById("quick-search-container")
const quickSearchInput = document.getElementById("quick-search")
const quickSearchDropdown = document.getElementById("search-dropdown")


const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
return new bootstrap.Tooltip(tooltipTriggerEl)
})


function initializePasswordInputs(){

    const passwordInputs = document.querySelectorAll('input[type="password"]');

    passwordInputs.forEach((passwordInput) => {
        // Create a container div 
        const container = passwordInput.parentElement
        // Create a toggle button
        const toggleButton = document.createElement('button');

        toggleButton.classList.add("btn", "btn-outline-secondary", "toggle-password");
        toggleButton.innerHTML = '<i class="bi bi-eye-slash"></i>';
        
        // Append the elements to the container
        container.appendChild(toggleButton);
      
        toggleButton.addEventListener('click', (e) => {
            e.preventDefault()
            togglePasswordVisibility(toggleButton, passwordInput);
        });
      })
}



function togglePasswordVisibility(toggleButton, inputElement) {
    if (inputElement.type === "password") {
      inputElement.type = "text";
      toggleButton.innerHTML = '<i class="bi bi-eye"></i>';
    } else {
      inputElement.type = "password";
      toggleButton.innerHTML = '<i class="bi bi-eye-slash"></i>';
    }
}

initializePasswordInputs()


let searchDropdownIndex = -1

function intializeQuickSearch(){

	document.addEventListener("keydown", (e) => {

        const isCtrlPressed = (e.ctrlKey || e.metaKey)
		
		if (isCtrlPressed && e.key == "k"){
			e.preventDefault();
			e.stopPropagation();
			showQuickSearch()
		}

		if (e.key == "Escape"){
			hideQuickSearch()
		}

	})

	document.addEventListener("click", (e) => {

		if (!quickSearchContainer.contains(e.target)){
			hideQuickSearch()
		}

	})

	updateQuickSearch(quickSearchData)

	quickSearchContainer.addEventListener('keydown', function (e) {
		
		if (e.key === 'ArrowUp' && searchDropdownIndex > 0) {
			searchDropdownIndex -= 1
		} else if (e.key === 'ArrowDown' && searchDropdownIndex < quickSearchDropdown.children.length - 1) {
			searchDropdownIndex += 1
		}else if (e.key === 'Enter'){
			const options = quickSearchDropdown.children;
			options[searchDropdownIndex]?.click()

			hideQuickSearch()
		}

		updateSelectedOption()
	})
	
	quickSearchContainer.addEventListener('mousemove', function (e) {
		const option = e.target
		if (option.tagName === 'A') {
		  searchDropdownIndex = Array.from(quickSearchDropdown.children).indexOf(option)
		  updateSelectedOption()
		}
	})

}

function updateQuickSearch(data){

	while (quickSearchDropdown.firstChild) {
		quickSearchDropdown.firstChild.remove()
	}
	for (let x of data){
		let link = document.createElement(`a`)
		link.innerText = x.title
		link.href = x.url
		link.onclick = hideQuickSearch

		quickSearchDropdown.appendChild(link)
	}

	if (data && quickSearchDropdown.children.length > 0){
		quickSearchDropdown.children[0].classList.add("search-active")
		searchDropdownIndex = 0
	}else{
		searchDropdownIndex = -1
	}
}


function updateSelectedOption() {
	const options = quickSearchDropdown.children;

	for (let i = 0; i < options.length; i++) {
	  options[i].classList.remove('search-active');
	}

	if (searchDropdownIndex !== -1) {
	  options[searchDropdownIndex].classList.add('search-active');
	}
}

function showQuickSearch(){
	event?.preventDefault()
	event?.stopPropagation()

	quickSearchContainer.classList.remove("!tw-hidden")
	quickSearchInput.focus()
	navSearch.classList.add("!tw-hidden")
}

function hideQuickSearch(){
	quickSearchContainer.classList.add("!tw-hidden")
	navSearch.classList.remove("!tw-hidden")
	console.log("hidden")
}

quickSearchInput.oninput = (e) => {

	const value = e.target.value
	const searchResults = []
	if (value.trim().length === 0){
		updateQuickSearch(quickSearchData)
	}

	for (let x of quickSearchData){
		if (x.title.toLowerCase().startsWith(value.toLowerCase())){
			searchResults.push(x)
		}
	}

	for (let x of quickSearchData){
		const isInArray = _.some(searchResults, (item) => _.isEqual(item, x))
		if (x.title.toLowerCase().includes(value.toLowerCase()) && !isInArray){
			searchResults.push(x)
		}
	}
	
	updateQuickSearch(searchResults)

	if (searchResults.length === 0){
		let link = document.createElement(`p`)
		link.innerText = "oops no search results found :("
		link.classList.add("tw-w-full", "tw-text-center", "tw-mt-[10%]")
		quickSearchDropdown.appendChild(link)

	}

}

intializeQuickSearch()


function openNav(){

	const navBar = document.getElementById("navbar") 

	navBar.classList.remove("tw-hidden")

}	

function closeNav(){
	const navBar = document.getElementById("navbar") 

	navBar.classList.add("tw-hidden")
}
