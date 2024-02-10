const incrementFormNum = (num) => ++num;

function addForm(e, formType, prefix, formNum, buttonType, emptyFormNum, totalForms){
    e.preventDefault()

    let newForm = formType[emptyFormNum].cloneNode(true)
    let formRegex = RegExp(`${prefix}-(\\d){1}-`,'g')
    console.log(formRegex)

    //undergraduateFormNum++ //this works
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `${prefix}-${formNum}-`)
    newForm.style.display = 'block' //copied form is hidden
    console.log(newForm)
    container.insertBefore(newForm, buttonType)
        
    totalForms.setAttribute('value', `${formNum+1}`)
}

function hideForm(e){
    if(e.target.checked && e.target.classList.contains("deleteCheckbox")){
        console.log("delete")
        //form = e.target.closest("div")
        form = e.target.closest(".entire-form")
        form.style.display = 'none'
    }
}