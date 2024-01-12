from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Application, User, Contact_information, Undergraduate, Postgraduate, Foreign_language, Work_experience, Reference_letter, Scholarship, Theses
from .forms import (UserRegisterForm, UserApplicationForm, ContactInformationForm, 
                    UndergraduateFormSet, PostgraduateFormSet, ForeignLanguageFormSet, WorkExperienceFormSet, ReferenceLetterFormSet, ScholarshipFormSet, ThesesFormSet)
from django.contrib.auth import authenticate, login, logout

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
    contact_information = Contact_information.objects.get(user=user)
    undergraduate_info = Undergraduate.objects.filter(user=user)
    postgraduate_info = Postgraduate.objects.filter(user=user)
    foreign_language_info = Foreign_language.objects.filter(user=user)
    work_experience_info = Work_experience.objects.filter(user=user)
    reference_letter_info = Reference_letter.objects.filter(user=user)
    scholarship_info = Scholarship.objects.filter(user=user)
    theses_info = Theses.objects.filter(user=user)
    context = {'application': application, 
               'user': user, 
               'contact_information': contact_information, 
               'undergraduate_info': undergraduate_info, 
               'postgraduate_info': postgraduate_info,
               'foreign_language_info': foreign_language_info,
               'work_experience_info': work_experience_info,
               'reference_letter_info': reference_letter_info,
               'scholarship_info': scholarship_info,
               'theses_info': theses_info
               }
    return render(request, "main/application.html", context)


@login_required(login_url='login') #maybe delete later. Needed because create application link was available before login
def create_application(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    user_form = UserApplicationForm()
    contact_info_form = ContactInformationForm()
    #prefix is used because more than one formsets will be displayed on the page
    undergraduate_formset = UndergraduateFormSet(queryset=Undergraduate.objects.none(), prefix = 'undergraduate')
    print(Undergraduate._meta.get_fields())
    postgraduate_formset = PostgraduateFormSet(queryset=Postgraduate.objects.none(), prefix = 'postgraduate')
    foreign_language_formset = ForeignLanguageFormSet(queryset=Foreign_language.objects.none(), prefix = 'foreign_language')
    work_experience_formset = WorkExperienceFormSet(queryset=Work_experience.objects.none(), prefix = 'work_experience')
    reference_letter_formset = ReferenceLetterFormSet(queryset=Reference_letter.objects.none(), prefix = 'reference_letter')
    scholarship_formset = ScholarshipFormSet(queryset=Scholarship.objects.none(), prefix = 'scholarship')
    theses_formset = ThesesFormSet(queryset=Theses.objects.none(), prefix = 'theses')
    
    if request.method == 'POST': 
        print(list(request.POST.items()))
        user_form = UserApplicationForm(request.POST, instance = request.user) #use instance because user object has already been created on register
        contact_info_form = ContactInformationForm(request.POST)
        undergraduate_formset = UndergraduateFormSet(request.POST, prefix = 'undergraduate')
        postgraduate_formset = PostgraduateFormSet(request.POST, prefix = 'postgraduate')
        foreign_language_formset = ForeignLanguageFormSet(request.POST, prefix = 'foreign_language')
        work_experience_formset = WorkExperienceFormSet(request.POST, prefix = 'work_experience')
        reference_letter_formset = ReferenceLetterFormSet(request.POST, prefix = 'reference_letter')
        scholarship_formset = ScholarshipFormSet(request.POST, prefix = 'scholarship')
        theses_formset = ThesesFormSet(request.POST, prefix = 'theses')

        if user_form.is_valid() and contact_info_form.is_valid() and undergraduate_formset.is_valid() and postgraduate_formset.is_valid() and \
            foreign_language_formset.is_valid() and work_experience_formset.is_valid() and reference_letter_formset.is_valid() and \
            scholarship_formset.is_valid() and theses_formset.is_valid():
           
            user_form.save()
            
            contact_info = contact_info_form.save(commit = False)
            contact_info.user = request.user
            contact_info.save()

            for form in undergraduate_formset:
                if form.has_changed():#ignore empty forms
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        undergraduate_info = form.save(commit = False)
                        undergraduate_info.user = request.user
                        undergraduate_info.save()

            for form in postgraduate_formset:
                if form.has_changed(): #ignore empty formsets
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        postgraduate_info = form.save(commit = False)
                        postgraduate_info.user = request.user
                        postgraduate_info.save()  

            for form in foreign_language_formset:
                if form.has_changed(): #ignore empty formsets   
                    form_is_deleted = form.cleaned_data['is_deleted']           
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        foreign_language_info = form.save(commit = False)
                        foreign_language_info.user = request.user
                        foreign_language_info.save()  

            for form in work_experience_formset:
                if form.has_changed(): #ignore empty formsets   
                    form_is_deleted = form.cleaned_data['is_deleted']           
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        work_experience_info = form.save(commit = False)
                        work_experience_info.user = request.user
                        work_experience_info.save()

            for form in reference_letter_formset:
                if form.has_changed(): #ignore empty formsets   
                    form_is_deleted = form.cleaned_data['is_deleted']           
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        reference_letter_info = form.save(commit = False)
                        reference_letter_info.user = request.user
                        reference_letter_info.save() 

            for form in scholarship_formset:
                if form.has_changed(): #ignore empty formsets   
                    form_is_deleted = form.cleaned_data['is_deleted']           
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        scholarship_info = form.save(commit = False)
                        scholarship_info.user = request.user
                        scholarship_info.save()

            for form in theses_formset:
                if form.has_changed(): #ignore empty formsets   
                    form_is_deleted = form.cleaned_data['is_deleted']           
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        theses_info = form.save(commit = False)
                        theses_info.user = request.user
                        theses_info.save()            
                 
            application = Application(user=request.user)
            application.save()
            request.user.has_applied = True
            request.user.save()              
                
            return redirect('my_application')

        else: #htmx
            print("something not right")

        if not work_experience_formset.is_valid():  
            print(work_experience_formset.errors)  

        if not reference_letter_formset.is_valid():  
            print(reference_letter_formset.errors)   

        if not undergraduate_formset.is_valid():  
            print(undergraduate_formset.errors) 
              
                
    context = {'user_form': user_form, 
               'contact_info_form': contact_info_form, 
               'undergraduate_formset': undergraduate_formset,
               'postgraduate_formset': postgraduate_formset, 
               'foreign_language_formset': foreign_language_formset, 
               'work_experience_formset': work_experience_formset,
               'reference_letter_formset': reference_letter_formset,
               'scholarship_formset': scholarship_formset,
               'theses_formset': theses_formset}
    return render(request, "main/application_form.html", context)   


@login_required(login_url='login')
def update_application(request, pk): #change an application that has already been created
    application = Application.objects.get(id=pk)
    user = User.objects.get(application=application)
    user_form = UserApplicationForm(instance = user) #populate with existing data
    contact_info_form = ContactInformationForm(instance = Contact_information.objects.get(user=user))
    undergraduate_formset = UndergraduateFormSet(instance = user)
    postgraduate_formset = PostgraduateFormSet(instance = user)
    foreign_language_formset = ForeignLanguageFormSet(instance = user)
    work_experience_formset = WorkExperienceFormSet(instance = user)
    reference_letter_formset = ReferenceLetterFormSet(instance = user)
    scholarship_formset = ScholarshipFormSet(instance = user)
    theses_formset = ThesesFormSet(instance = user)

    if request.method == 'POST':
        print(list(request.POST.items()))
        user_form = UserApplicationForm(request.POST, instance = user)
        contact_info_form = ContactInformationForm(request.POST, instance = Contact_information.objects.get(user=user)) 
        undergraduate_formset = UndergraduateFormSet(request.POST, instance = user)
        postgraduate_formset = PostgraduateFormSet(request.POST, instance = user)
        foreign_language_formset = ForeignLanguageFormSet(request.POST, instance = user)
        work_experience_formset = WorkExperienceFormSet(request.POST, instance = user)
        reference_letter_formset = ReferenceLetterFormSet(request.POST, instance = user)
        scholarship_formset = ScholarshipFormSet(request.POST, instance = user)
        theses_formset = ThesesFormSet(request.POST, instance = user)

        if user_form.is_valid() and contact_info_form.is_valid() and undergraduate_formset.is_valid() and postgraduate_formset.is_valid() and \
            foreign_language_formset.is_valid() and work_experience_formset.is_valid() and reference_letter_formset.is_valid() and \
            scholarship_formset.is_valid() and theses_formset.is_valid():
            
            user_form.save()
            
            contact_info_form.save()  
            
            for form in undergraduate_formset:
                if form.has_changed():
                    #form.delete() #does not work. Throws error. Can't delete db data using post request data. 
                    #Data needs to be saved to db first (would work if formset can_delete=True) 
                    form.save()
            undergraduate_info = Undergraduate.objects.filter(user=user)
            undergraduate_info_to_be_deleted = undergraduate_info.filter(is_deleted=True)
            for form in undergraduate_info_to_be_deleted:
                form.delete()
                      
            for form in postgraduate_formset:
                if form.has_changed():
                    form.save() 
            postgraduate_info = Postgraduate.objects.filter(user=user)
            postgraduate_info_to_be_deleted = postgraduate_info.filter(is_deleted=True)
            for form in postgraduate_info_to_be_deleted:
                form.delete()

            for form in foreign_language_formset:
                if form.has_changed():
                    form.save() 
            foreign_language_info = Foreign_language.objects.filter(user=user)
            foreign_language_info_to_be_deleted = foreign_language_info.filter(is_deleted=True)
            for form in foreign_language_info_to_be_deleted:
                form.delete()

            for form in work_experience_formset:
                if form.has_changed():
                    form.save() 
            work_experience_info = Work_experience.objects.filter(user=user)
            work_experience_info_to_be_deleted = work_experience_info.filter(is_deleted=True)
            for form in work_experience_info_to_be_deleted:
                form.delete()

            for form in reference_letter_formset:
                if form.has_changed():
                    form.save() 
            reference_letter_info = Reference_letter.objects.filter(user=user)
            reference_letter_info_to_be_deleted = reference_letter_info.filter(is_deleted=True)
            for form in reference_letter_info_to_be_deleted:
                form.delete()  

            for form in scholarship_formset:
                if form.has_changed():
                    form.save() 
            scholarship_info = Scholarship.objects.filter(user=user)
            scholarship_info_to_be_deleted = scholarship_info.filter(is_deleted=True)
            for form in scholarship_info_to_be_deleted:
                form.delete()  

            for form in theses_formset:
                if form.has_changed():
                    form.save() 
            theses_info = Theses.objects.filter(user=user)
            theses_info_to_be_deleted = theses_info.filter(is_deleted=True)
            for form in theses_info_to_be_deleted:
                form.delete()     
                 
            application.save() #used in order to change updated field in application model
            return redirect('my_application') 
        else:
            print("not valid") #debugging   
    context = {'user_form': user_form, 
               'contact_info_form': contact_info_form, 
               'undergraduate_formset': undergraduate_formset, 
               'postgraduate_formset': postgraduate_formset, 
               'foreign_language_formset': foreign_language_formset,
               'work_experience_formset': work_experience_formset,
               'reference_letter_formset': reference_letter_formset,
               'scholarship_formset': scholarship_formset,
               'theses_formset': theses_formset}
    return render(request, "main/application_form.html", context)


@login_required(login_url='login') #maybe delete later
def delete_application(request, pk): #delete an application
    application = Application.objects.get(id=pk)
    context = {'obj': application}

    if request.method == 'POST':
        user = User.objects.get(application=application)
        user.has_applied = False
        user.save()
        contact_information = Contact_information.objects.get(user=user)
        contact_information.delete()
        undergraduate_info = Undergraduate.objects.filter(user=user)
        postgraduate_info = Postgraduate.objects.filter(user=user)
        foreign_language_info = Foreign_language.objects.filter(user=user)
        work_experience_info = Work_experience.objects.filter(user=user)
        reference_letter_info = Reference_letter.objects.filter(user=user)
        scholarship_info = Scholarship.objects.filter(user=user)
        theses_info = Theses.objects.filter(user=user)

        for form in undergraduate_info:
            form.delete()
        
        for form in postgraduate_info:
            form.delete()

        for form in foreign_language_info:
            form.delete()    

        for form in work_experience_info:
            form.delete()    

        for form in reference_letter_info:
            form.delete() 

        for form in scholarship_info:
            form.delete()     

        for form in theses_info:
            form.delete()      

        application.delete()
        #request.user.has_applied = False #will not work if admin can delete applications
        #request.user.save()
        return redirect('home')
    return render(request, "main/delete.html", context)   


@login_required(login_url='login')
def my_application(request): #shows current users application info
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    user=request.user
    contact_information = Contact_information.objects.get(user=user)
    undergraduate_info = Undergraduate.objects.filter(user=user)
    postgraduate_info = Postgraduate.objects.filter(user=user)
    foreign_language_info = Foreign_language.objects.filter(user=user)
    work_experience_info = Work_experience.objects.filter(user=user)
    reference_letter_info = Reference_letter.objects.filter(user=user)
    scholarship_info = Scholarship.objects.filter(user=user)
    theses_info = Theses.objects.filter(user=user)
    application = Application.objects.get(user=request.user)
    context = {'application': application, 
               'user': user, 
               'contact_information': contact_information, 
               'undergraduate_info': undergraduate_info, 
               'postgraduate_info': postgraduate_info, 
               'foreign_language_info': foreign_language_info, 
               'work_experience_info': work_experience_info,
               'reference_letter_info': reference_letter_info,
               'scholarship_info': scholarship_info,
               'theses_info': theses_info}
    return render(request, "main/my_application.html", context)




      
    