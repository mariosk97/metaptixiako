let container = document.querySelector("#form-container")
let scholarshipForm = document.querySelectorAll(".scholarship-form")
let addScholarshipButton = document.querySelector("#add_scholarship_form")
let scholarshipFormNum = scholarshipForm.length-1
let emptyScholarshipFormNum = scholarshipFormNum
let scholarshipPrefix = "scholarship"
let totalScholarshipForms = document.querySelector("#id_scholarship-TOTAL_FORMS")
//first form is hidden so there is always an empty form to be copied by addForm if page is refreshed because of validation errors plus user has deleted all forms
//only works for create because if user is trying to update, the first form might not be empty
if (!(window.location.href.indexOf("update") > -1)) { //if url does not contain 'update', user is trying to create an application
    console.log("create")
    scholarshipForm[0].style.display = 'none' 
}  
 

addScholarshipButton.addEventListener('click', (e) => {    
    scholarshipFormNum = incrementFormNum(scholarshipFormNum);
    console.log("scholarshipFormNum: " + scholarshipFormNum);
    addForm(e, scholarshipForm, scholarshipPrefix, scholarshipFormNum, addScholarshipButton, emptyScholarshipFormNum, totalScholarshipForms); 
});

container.addEventListener('change', e => {
    hideForm(e)
});