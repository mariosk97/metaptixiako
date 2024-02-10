let container = document.querySelector("#form-container")
let undergraduateForm = document.querySelectorAll(".undergraduate-form")
console.log(undergraduateForm)
let addUndergraduateButton = document.querySelector("#add_undergraduate_form")
//let totalUndergraduateForms = document.querySelector("#id_undergraduate_set-TOTAL_FORMS") //works()
//console.log(totalUndergraduateForms)
let undergraduateFormNum = undergraduateForm.length-1
console.log("undergraduateFormNum: " + undergraduateFormNum)
//emptyUndergraduateFormNum does not and should not change, because the form that is cloned needs to be an empty one that 
//hasnt been inserted to the db (otherwise error is raised). So the only form that can be cloned is the one that was last when the page was loaded.
let emptyUndergraduateFormNum = undergraduateFormNum 
console.log("emptyUndergraduateFormNum: " + emptyUndergraduateFormNum)
//let undergraduatePrefix = "undergraduate_set" //works()
//addUndergraduateButton.addEventListener('click', addForm) //this works
let undergraduatePrefix = "undergraduate"
let totalUndergraduateForms = document.querySelector("#id_undergraduate-TOTAL_FORMS")
//first form is hidden so there is always an empty form to be copied by addForm if page is refreshed because of validation errors plus user has deleted all forms
//only works for create because if user is trying to update, the first form might not be empty
if (!(window.location.href.indexOf("update") > -1)) { //if url does not contain 'update', user is trying to create an application
    console.log("create")
    undergraduateForm[0].style.display = 'none' 
}    

addUndergraduateButton.addEventListener('click', (e) => {    
    undergraduateFormNum = incrementFormNum(undergraduateFormNum);
    console.log("undergraduateFormNum: " + undergraduateFormNum);
    addForm(e, undergraduateForm, undergraduatePrefix, undergraduateFormNum, addUndergraduateButton, emptyUndergraduateFormNum, totalUndergraduateForms); 
});

container.addEventListener('change', e => {
    hideForm(e)
});