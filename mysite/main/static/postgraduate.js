let container = document.querySelector("#form-container")
let postgraduateForm = document.querySelectorAll(".postgraduate-form")
let addPostgraduateButton = document.querySelector("#add_postgraduate_form")
let postgraduateFormNum = postgraduateForm.length-1
let emptyPostgraduateFormNum = postgraduateFormNum 
console.log("emptyPostgraduateFormNum: " + emptyPostgraduateFormNum)
let postgraduatePrefix = "postgraduate"
let totalPostgraduateForms = document.querySelector("#id_postgraduate-TOTAL_FORMS")
//first form is hidden so there is always an empty form to be copied by addForm if page is refreshed because of validation errors plus user has deleted all forms
//only works for create because if user is trying to update, the first form might not be empty
if (!(window.location.href.indexOf("update") > -1)) { //if url does not contain 'update', user is trying to create an application
    console.log("create")
    postgraduateForm[0].style.display = 'none' 
}  

addPostgraduateButton.addEventListener('click', (e) => {    
    postgraduateFormNum = incrementFormNum(postgraduateFormNum);
    console.log("postgraduateFormNum: " + postgraduateFormNum);
    addForm(e, postgraduateForm, postgraduatePrefix, postgraduateFormNum, addPostgraduateButton, emptyPostgraduateFormNum, totalPostgraduateForms); 
});

container.addEventListener('change', e => {
    hideForm(e)
});