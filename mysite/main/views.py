from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Application, User, Contact_information
from .forms import ApplicationForm, UserRegisterForm, UserApplicationForm, ContactInformationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:    
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)   
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Username or password is incorrect')    
    context = {'page': page}
    return render(request, "main/login_register.html", context)

def logout_user(request):
    logout(request)
    return redirect('home')   

def register_page(request):
    #form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')    
    context = {'form': form}
    return render(request, "main/login_register.html", context)  

def home(request):
    return render(request, "main/base.html", {})

def applications(request): #list of all applications  
    applications = Application.objects.all()
    context = {'applications': applications}
    return render(request, "main/applications.html", context)    

def application(request, pk): #info about a specific application
    application = Application.objects.get(id=pk)
    user = User.objects.get(application=application)
    context = {'application': application, 'user': user}
    return render(request, "main/application.html", context)

@login_required(login_url='login') #maybe delete later. Needed because create application link was available before login
def create_application(request):
    #form = ApplicationForm()
    if request.user.is_superuser:
        return redirect('home')
    user_form = UserApplicationForm()
    contact_info_form = ContactInformationForm()
    if request.method == 'POST': 
        if 'user_info' in request.POST: 
            user_form = UserApplicationForm(request.POST, instance = request.user)
            if user_form.is_valid():
                user_form.save()
            #application = Application(user=request.user, name='Beatles Blog', description='Test')
                application = Application(user=request.user)
                application.save()
                request.user.has_applied = True
                request.user.save()
                #return redirect('home')
        if 'contact_info' in request.POST:   
            contact_info_form = ContactInformationForm(request.POST)
            if contact_info_form.is_valid():
                contact_info = contact_info_form.save(commit = False)
                contact_info.user = request.user
                contact_info.save()
    context = {'user_form': user_form, 'contact_info_form': contact_info_form}
    return render(request, "main/application_form.html", context)   

@login_required(login_url='login')
def update_application(request, pk): #change an application that has already been created
    application = Application.objects.get(id=pk)
    user = User.objects.get(application=application)
    user_form = UserApplicationForm(instance = user) #populate with existing data
    contact_info_form = ContactInformationForm(instance = Contact_information.objects.get(user=user))
    if request.method == 'POST':
        #form = ApplicationForm(request.POST, instance = application)
        if 'user_info' in request.POST:
            user_form = UserApplicationForm(request.POST, instance = user)
            if user_form.is_valid():
                user_form.save()
                application.save() #used in order to change updated field in application model
                #return redirect('home')
        if 'contact_info' in request.POST:   
            contact_info_form = ContactInformationForm(request.POST, instance = user)
            if contact_info_form.is_valid():
                contact_info_form.save()  
                application.save()  
    context = {'user_form': user_form, 'contact_info_form': contact_info_form}
    return render(request, "main/application_form.html", context)

@login_required(login_url='login') #maybe delete later
def delete_application(request, pk): #delete an application
    application = Application.objects.get(id=pk)
    context = {'obj': application}
    if request.method == 'POST':
        user = User.objects.get(application=application)
        user.has_applied = False
        user.save()
        application.delete()
        #request.user.has_applied = False #will not work if admin can delete applications
        #request.user.save()
        return redirect('home')
    return render(request, "main/delete.html", context)   

@login_required(login_url='login')
def my_application(request): #shows current users application info
    user=request.user
    application = Application.objects.get(user=request.user)
    context = {'application': application, 'user': user}
    return render(request, "main/my_application.html", context)

      
    