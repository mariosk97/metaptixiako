from django.forms import ModelForm
from django import forms
from .models import Application, User, Contact_information
from django.contrib.auth.forms import UserCreationForm

class ApplicationForm (ModelForm): #currently not used. Done with UserApplicationForm
    class Meta:
        model = Application
        #fields = '__all__'
        exclude = ['user'] #automatically assigned from create application view

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User  
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']  

class UserApplicationForm(ModelForm):
    user_info = forms.BooleanField(widget=forms.HiddenInput, initial=True) #used to identify form in create_application view. Field is irrelevant.

    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'fathers_name', 'mothers_name', 'sex', 'place_of_birth', 'prefecture', 'country', 'marital_status', 'military_service', 'date_of_birth', 'amka' , 'afm']       
            
class ContactInformationForm(ModelForm):
    contact_info = forms.BooleanField(widget=forms.HiddenInput, initial=True) #used to identify form in create_application view. Field is irrelevant.

    class Meta:
        model = Contact_information  
        fields = ['home_number', 'cell_number']
        exclude = ['user'] #automatically assigned from create application view
