from django.forms import ModelForm
from django.forms import modelformset_factory, inlineformset_factory
from django import forms
from .models import Application, User, Contact_information, Undergraduate, Postgraduate, Studies, Foreign_language, Work_experience, Reference_letter, Scholarship, Theses, Masters, Orientation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .fields import ListTextWidget

class ApplicationForm (ModelForm): #currently not used. Done with UserApplicationForm. Delete
    class Meta:
        model = Application
        #fields = '__all__'
        exclude = ['user'] #automatically assigned from create application view


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User  
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']  
        

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None    


class UserApplicationForm(ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User  
        fields = ['first_name', 'last_name','email', 'fathers_name', 'mothers_name', 'sex', 'place_of_birth', 'prefecture', 'country', 'marital_status', 'military_service', 'date_of_birth', 'amka' , 'afm']       
            
    

class ContactInformationForm(ModelForm):

    class Meta:
        model = Contact_information  
        fields = ['home_number', 'cell_number']
        exclude = ['user'] #automatically assigned from create application view


class StudyForm(ModelForm): 
    
    class Meta:
        model = Studies
        exclude = ['user'] #automatically assigned from create application view
        labels = {
            "is_deleted": "Delete",
            "univercity": "Univercity*",
            "department": "Department*",
            "degree_title": "Degree Title"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_deleted"].widget.attrs.update({"class": "deleteCheckbox"})   

    #used to validate a form only if it has not been deleted. Otherwise a half-filled form that was later deleted might raise errors, which shouldn't happen
    def clean(self):
        degree_title = self.cleaned_data.get("degree_title")   
        grade = self.cleaned_data.get("grade")
        univercity = self.cleaned_data.get("univercity")
        department = self.cleaned_data.get("department")
        is_deleted = self.cleaned_data.get("is_deleted")

        if not is_deleted: #if user has deleted the form no validation is required
            if degree_title is not None or grade is not None or univercity is not None or department is not None: #if user has filled at least one of the fields
                if univercity is None or department is None: #if univercity or department have not been filled
                    raise ValidationError(
                        "Univercity and department are required."
                    )   
                

UndergraduateFormSet = inlineformset_factory(
    User, Undergraduate, form=StudyForm, extra=1, can_delete = False
)   


PostgraduateFormSet = inlineformset_factory(
    User, Postgraduate, form=StudyForm, extra=1, can_delete = False
)  


class ForeignLanguageForm(ModelForm): 
    acquisition_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Foreign_language
        exclude = ['user'] #automatically assigned from create application view
        labels = {
            "is_deleted": "Delete",
            "language": "Language*",
            "degree": "Degree*",
            "acquisition_date": "Acquisition Date*"
        }

    def __init__(self, *args, **kwargs):
        _language_list = kwargs.pop('language_data_list', None) #now the form needs a parameter when a new instance is created in views.py
        _level_list = kwargs.pop('level_data_list', None)
        super().__init__(*args, **kwargs)
        self.fields["is_deleted"].widget.attrs.update({"class": "deleteCheckbox"}) 
        
        self.fields['language'].widget = ListTextWidget(data_list=_language_list, name='language-list') 
        self.fields['level'].widget = ListTextWidget(data_list=_level_list, name='level-list') 

    #used to validate a form only if it has not been deleted. Otherwise a half-filled form that was later deleted might raise errors, which shouldn't happen
    def clean(self):
        language = self.cleaned_data.get("language")
        level = self.cleaned_data.get("level")  
        degree = self.cleaned_data.get("degree")  
        grade = self.cleaned_data.get("grade")  
        acquisition_date = self.cleaned_data.get("acquisition_date") 
        is_deleted = self.cleaned_data.get("is_deleted")  

        if not is_deleted: #if user has deleted the form no validation is required
            if language is not None or level is not None or degree is not None or grade is not None or acquisition_date is not None: #if user has filled at least one of the fields
                if language is None or degree is None or acquisition_date is None: #if language, degree or acquisition_date have not been filled
                    raise ValidationError(
                        "Language, degree and acquisition date are required."
                    )          


ForeignLanguageFormSet = inlineformset_factory(
    User, Foreign_language, form=ForeignLanguageForm, extra=1, can_delete = False
)       


class WorkExperienceForm(ModelForm): 
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Work_experience
        exclude = ['user'] #automatically assigned from create application view
        labels = {
            "is_deleted": "Delete",
            "start_date": "Start Date*",
            "company": "Company*",
            "position": "Position*"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_deleted"].widget.attrs.update({"class": "deleteCheckbox"}) 

    #used to validate a form only if it has not been deleted. Otherwise a half-filled form that was later deleted might raise errors, which shouldn't happen
    def clean(self):
        start_date = self.cleaned_data.get("start_date")    
        end_date = self.cleaned_data.get("end_date") 
        company = self.cleaned_data.get("company") 
        position = self.cleaned_data.get("position")  
        is_deleted = self.cleaned_data.get("is_deleted")

        if not is_deleted: #if user has deleted the form no validation is required
            if start_date is not None or end_date is not None or company is not None or position is not None: #if user has filled at least one of the fields
                if start_date is None or company is None or position is None: #if start_date, company or position have not been filled
                    raise ValidationError(
                        "Start date, company and position are required."
                    ) 


WorkExperienceFormSet = inlineformset_factory(
    User, Work_experience, form=WorkExperienceForm, extra=1, can_delete = False
)            


class ReferenceLetterForm(ModelForm): 
    
    class Meta:
        model = Reference_letter
        exclude = ['user'] #automatically assigned from create application view
        labels = {
            "is_deleted": "Delete",
            "full_name": "Full Name*",
            "position": "Position*",
            "organization": "Organization*",
            "email": "Email*"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_deleted"].widget.attrs.update({"class": "deleteCheckbox"}) 

    #used to validate a form only if it has not been deleted. Otherwise a half-filled form that was later deleted might raise errors, which shouldn't happen
    def clean(self):
        full_name = self.cleaned_data.get("full_name") 
        position = self.cleaned_data.get("position")   
        organization = self.cleaned_data.get("organization")
        email = self.cleaned_data.get("email")   
        is_deleted = self.cleaned_data.get("is_deleted")

        if not is_deleted: #if user has deleted the form no validation is required
            if full_name is not None or position is not None or organization is not None or email is not None: #if user has filled at least one of the fields
                if full_name is None or position is None or organization is None or email is None: #if any has not been filled
                    raise ValidationError(
                        "All fields are required."
                    )  


ReferenceLetterFormSet = inlineformset_factory(
    User, Reference_letter, form=ReferenceLetterForm, extra=1, can_delete = False
)


class ScholarshipForm(ModelForm): 
    acquisition_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Scholarship
        exclude = ['user'] #automatically assigned from create application view
        labels = {
            "is_deleted": "Delete",
            "description": "Description*",
            "educational_institution": "Educational Institution*"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_deleted"].widget.attrs.update({"class": "deleteCheckbox"}) 

    #used to validate a form only if it has not been deleted. Otherwise a half-filled form that was later deleted might raise errors, which shouldn't happen
    def clean(self):
        description = self.cleaned_data.get("description") 
        acquisition_date = self.cleaned_data.get("acquisition_date") 
        educational_institution = self.cleaned_data.get("educational_institution") 
        is_deleted = self.cleaned_data.get("is_deleted")  

        if not is_deleted: #if user has deleted the form no validation is required
            if description is not None or acquisition_date is not None or educational_institution is not None: #if user has filled at least one of the fields
                if description is None or educational_institution is None: #if description or educational_institution have not been filled
                    raise ValidationError(
                        "Description and educational institution are required."
                    )   


ScholarshipFormSet = inlineformset_factory(
    User, Scholarship, form=ScholarshipForm, extra=1, can_delete = False
)


class ThesesForm(ModelForm): 
    
    class Meta:
        model = Theses
        exclude = ['user'] #automatically assigned from create application view
        labels = {
            "is_deleted": "Delete",
            "title": "Title*"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_deleted"].widget.attrs.update({"class": "deleteCheckbox"}) 

    #used to validate a form only if it has not been deleted. Otherwise a half-filled form that was later deleted might raise errors, which shouldn't happen
    def clean(self):
        title = self.cleaned_data.get("title")
        supervisor = self.cleaned_data.get("supervisor")
        grade = self.cleaned_data.get("grade")
        is_deleted = self.cleaned_data.get("is_deleted")

        if not is_deleted: #if user has deleted the form no validation is required
            if title is not None or supervisor is not None or grade is not None: #if user has filled at least one of the fields
                if title is None: #if title has not been filled
                    raise ValidationError(
                        "Title is required."
                    )   


ThesesFormSet = inlineformset_factory(
    User, Theses, form=ThesesForm, extra=1, can_delete = False
)


class MastersForm(ModelForm): 
    name = forms.ModelChoiceField(queryset = Masters.objects.all())

    class Meta:
        model = Masters
        exclude = ['user'] #automatically assigned from create application view


class OrientationForm(ModelForm): 
    name = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Masters
        exclude = ['user'] #automatically assigned from create application view   


    def __init__(self, masters, *args, **kwargs):
        super(OrientationForm, self).__init__(*args, **kwargs)
        self.fields['name'].queryset = Orientation.objects.filter(masters=masters)         
           

       