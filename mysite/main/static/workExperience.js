let container = document.querySelector("#form-container")
let workExperienceForm = document.querySelectorAll(".work_experience-form")
let addWorkExperienceButton = document.querySelector("#add_work_experience_form")
let workExperienceFormNum = workExperienceForm.length-1
let emptyWorkExperienceFormNum = workExperienceFormNum
let workExperiencePrefix = "work_experience"
let totalWorkExperienceForms = document.querySelector("#id_work_experience-TOTAL_FORMS")
//first form is hidden so there is always an empty form to be copied by addForm if page is refreshed because of validation errors plus user has deleted all forms
//only works for create because if user is trying to update, the first form might not be empty
if (!(window.location.href.indexOf("update") > -1)) { //if url does not contain 'update', user is trying to create an application
    console.log("create")
    workExperienceForm[0].style.display = 'none'
}  
 

addWorkExperienceButton.addEventListener('click', (e) => {    
    workExperienceFormNum = incrementFormNum(workExperienceFormNum);
    console.log("workExperienceFormNum: " + workExperienceFormNum);
    addForm(e, workExperienceForm, workExperiencePrefix, workExperienceFormNum, addWorkExperienceButton, emptyWorkExperienceFormNum, totalWorkExperienceForms); 
});

container.addEventListener('change', e => {
    hideForm(e)
});