let container = document.querySelector("#form-container")
let thesesForm = document.querySelectorAll(".theses-form")
let addThesesButton = document.querySelector("#add_theses_form")
let thesesFormNum = thesesForm.length-1
let emptyThesesFormNum = thesesFormNum
let thesesPrefix = "theses"
let totalThesesForms = document.querySelector("#id_theses-TOTAL_FORMS")
//first form is hidden so there is always an empty form to be copied by addForm if page is refreshed because of validation errors plus user has deleted all forms
//only works for create because if user is trying to update, the first form might not be empty
if (!(window.location.href.indexOf("update") > -1)) { //if url does not contain 'update', user is trying to create an application
    console.log("create")
    thesesForm[0].style.display = 'none' 
}  
 

addThesesButton.addEventListener('click', (e) => {    
    thesesFormNum = incrementFormNum(thesesFormNum);
    console.log("thesesFormNum: " + thesesFormNum);
    addForm(e, thesesForm, thesesPrefix, thesesFormNum, addThesesButton, emptyThesesFormNum, totalThesesForms); 
});

container.addEventListener('change', e => {
    hideForm(e)
});