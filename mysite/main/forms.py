from django.forms import ModelForm
from .models import Application, User
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
    class Meta:
        model = User  
        fields = ['first_name', 'last_name',]       
            