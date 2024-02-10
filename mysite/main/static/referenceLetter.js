let container = document.querySelector("#form-container")
let referenceLetterForm = document.querySelectorAll(".reference_letter-form")
let addReferenceLetterButton = document.querySelector("#add_reference_letter_form")
let referenceLetterFormNum = referenceLetterForm.length-1
let emptyReferenceLetterFormNum = referenceLetterFormNum
let referenceLetterPrefix = "reference_letter"
let totalReferenceLetterForms = document.querySelector("#id_reference_letter-TOTAL_FORMS")
//first form is hidden so there is always an empty form to be copied by addForm if page is refreshed because of validation errors plus user has deleted all forms
//only works for create because if user is trying to update, the first form might not be empty
if (!(window.location.href.indexOf("update") > -1)) { //if url does not contain 'update', user is trying to create an application
    console.log("create")
    referenceLetterForm[0].style.display = 'none' 
}  


addReferenceLetterButton.addEventListener('click', (e) => {    
    referenceLetterFormNum = incrementFormNum(referenceLetterFormNum);
    console.log("referenceLetterFormNum: " + referenceLetterFormNum);
    addForm(e, referenceLetterForm, referenceLetterPrefix, referenceLetterFormNum, addReferenceLetterButton, emptyReferenceLetterFormNum, totalReferenceLetterForms); 
});

container.addEventListener('change', e => {
    hideForm(e)
});