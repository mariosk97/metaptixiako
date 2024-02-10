let container = document.querySelector("#form-container")
let foreignLanguageForm = document.querySelectorAll(".foreign_language-form")
let addForeignLanguageButton = document.querySelector("#add_foreign_language_form")
let foreignLanguageFormNum = foreignLanguageForm.length-1
let emptyForeignLanguageFormNum = foreignLanguageFormNum
let foreignLanguagePrefix = "foreign_language"
let totalForeignLanguageForms = document.querySelector("#id_foreign_language-TOTAL_FORMS")
//first form is hidden so there is always an empty form to be copied by addForm if page is refreshed because of validation errors plus user has deleted all forms
//only works for create because if user is trying to update, the first form might not be empty
if (!(window.location.href.indexOf("update") > -1)) { //if url does not contain 'update', user is trying to create an application
    console.log("create")
    foreignLanguageForm[0].style.display = 'none' 
}   

addForeignLanguageButton.addEventListener('click', (e) => {    
    foreignLanguageFormNum = incrementFormNum(foreignLanguageFormNum);
    console.log("foreignLanguageFormNum: " + foreignLanguageFormNum);
    addForm(e, foreignLanguageForm, foreignLanguagePrefix, foreignLanguageFormNum, addForeignLanguageButton, emptyForeignLanguageFormNum, totalForeignLanguageForms); 
});

container.addEventListener('change', e => {
    hideForm(e)
});