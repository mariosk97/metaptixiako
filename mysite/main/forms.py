from django.forms import ModelForm
from django.forms import modelformset_factory, inlineformset_factory
from django import forms
from .models import Application, User, Contact_information, Undergraduate, Postgraduate, Studies, Foreign_language
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class ApplicationForm (ModelForm): #currently not used. Done with UserApplicationForm
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
    ##user_info = forms.BooleanField(widget=forms.HiddenInput, initial=True) #used to identify form in create_application view. Field is irrelevant. #polla submit
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'fathers_name', 'mothers_name', 'sex', 'place_of_birth', 'prefecture', 'country', 'marital_status', 'military_service', 'date_of_birth', 'amka' , 'afm']       
            
    

class ContactInformationForm(ModelForm):
    ##contact_info_check = forms.BooleanField(widget=forms.HiddenInput, initial=True) #used to identify form in create_application view. Field is irrelevant. #polla submit

    class Meta:
        model = Contact_information  
        fields = ['home_number', 'cell_number']
        exclude = ['user'] #automatically assigned from create application view


class StudyForm(ModelForm): 
    
    class Meta:
        model = Studies
        #model = Undergraduate
        exclude = ['user'] #automatically assigned from create application view
        labels = {
            "is_deleted": "Delete"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_deleted"].widget.attrs.update({"class": "deleteCheckbox"})   
        #self.fields["DELETE"].widget.attrs.update({"class": "deleteCheckbox"})

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
                        "univercity and department are required."
                    )   
                

UndergraduateFormSet = inlineformset_factory(
    User, Undergraduate, form=StudyForm, extra=1, can_delete = False
    #exclude = ['user'] anti gia form = ... an dn douleuei
)   


PostgraduateFormSet = inlineformset_factory(
    User, Postgraduate, form=StudyForm, extra=1, can_delete = False
    #exclude = ['user'] anti gia form = ... an dn douleuei
)  


class ForeignLanguageForm(ModelForm): 
    
    class Meta:
        model = Foreign_language
        exclude = ['user'] #automatically assigned from create application view
        labels = {
            "is_deleted": "Delete"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_deleted"].widget.attrs.update({"class": "deleteCheckbox"})    


ForeignLanguageFormSet = inlineformset_factory(
    User, Foreign_language, form=ForeignLanguageForm, extra=1, can_delete = False
    #exclude = ['user'] anti gia form = ... an dn douleuei
)       
