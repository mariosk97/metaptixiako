from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Application, User, Contact_information, Undergraduate, Postgraduate, Foreign_language, Work_experience, Reference_letter, Scholarship, Theses, Master
from .forms import (UserRegisterForm, UserApplicationForm, ContactInformationForm, MasterForm, OrientationForm,
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
    if not request.user.has_perm("main.view_application"):
        return redirect('home')
    applications = Application.objects.all()
    context = {'applications': applications}
    return render(request, "main/applications.html", context)    


def application(request, pk): #info about a specific application
    if not request.user.has_perm("main.view_application"):
        return redirect('home')
    
    application = Application.objects.get(id=pk)
    user = User.objects.get(application=application)

    try:
        contact_information = Contact_information.objects.get(user=user)
    except Contact_information.DoesNotExist:
        contact_information = None

    undergraduate_info = Undergraduate.objects.filter(user=user)
    postgraduate_info = Postgraduate.objects.filter(user=user)
    foreign_language_info = Foreign_language.objects.filter(user=user)
    work_experience_info = Work_experience.objects.filter(user=user)
    reference_letter_info = Reference_letter.objects.filter(user=user)
    scholarship_info = Scholarship.objects.filter(user=user)
    theses_info = Theses.objects.filter(user=user)
    
    context = { 'user': user, 
               'application': application,
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

           
@login_required(login_url='login') 
def delete_application(request, pk): #delete an application
    application = Application.objects.get(id=pk)
    context = {'obj': application}

    if request.method == 'POST':
        
        user = User.objects.get(application=application)
        if not application.is_accepted: #accepted applications should not be deleted from the database
            application.delete()
        else:
            application.is_withdrawn = True 
            application.save()   
        
        users_applications = Application.objects.filter(user=user)
        number_of_applications = Application.objects.filter(user=user).count()
        number_of_withdrawn_applications = users_applications.filter(is_withdrawn=True).count()
        print(number_of_withdrawn_applications)
        print(number_of_applications)
        number_of_active_applications = number_of_applications - number_of_withdrawn_applications
        if number_of_active_applications == 0:
            user.has_applied = False
            user.save() 
            return redirect('home')
        else:
             return redirect('my_applications')

        #request.user.has_applied = False #will not work if admin can delete applications
        #request.user.save()
        
    return render(request, "main/delete.html", context)   


@login_required(login_url='login')
def my_applications(request): #shows current users application info
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user=request.user

    try:
        contact_information = Contact_information.objects.get(user=request.user)
    except Contact_information.DoesNotExist:
        contact_information = None 

    if contact_information is None:
        has_contact_info = False
    else:
        has_contact_info = True   

    try:
        applications = Application.objects.filter(user=request.user)
        applications = applications.filter(is_withdrawn=False)
    except Application.DoesNotExist:
        applications = None

    context = {'applications': applications, 
               'user': user,
               'has_contact_info': has_contact_info
            }
               
    return render(request, "main/my_applications.html", context)


@login_required(login_url='login') 
def validate_application(request, pk):
    if not request.user.has_perm("main.validate_application"):
        return redirect('home')
    
    application = Application.objects.get(id=pk)
    
    if request.method == 'POST':
        application.is_validated = True
        application.save()
        return redirect('all_applications')

    context = {'application': application}    

    return render(request, "main/validate.html", context)


@login_required(login_url='login') 
def accept_application(request, pk):
    if not request.user.has_perm("main.accept_application"):
        return redirect('home')
    
    application = Application.objects.get(id=pk)
    
    if request.method == 'POST':
        application.is_accepted = True
        application.save()
        return redirect('all_applications')

    context = {'application': application}    

    return render(request, "main/accept.html", context)


@login_required(login_url='login')
def user_information(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user_form = UserApplicationForm(instance = request.user) #some information was filled during registration so it should be populated with existing data

    if request.method == 'POST': 
        user_form = UserApplicationForm(request.POST, instance = request.user)
        if user_form.is_valid():
            user_form.save() 

            try:
                contact_information = Contact_information.objects.get(user=request.user)
            except Contact_information.DoesNotExist:
                contact_information = None           
                
            if contact_information is None:
                return redirect('contact_information') #user is trying to create
            else:
                return redirect('update_contact_information') #user is trying to update
        else:        
            print(user_form.errors)        

    context = {
        'user_form': user_form
    }

    return render(request, "main/user_information.html", context) 


login_required(login_url='login') 
def contact_information(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    contact_info_form = ContactInformationForm()

    if request.method == 'POST':
        contact_info_form = ContactInformationForm(request.POST)
        if contact_info_form.is_valid():
            
            #contact_info = contact_info_form.save(commit = False)
            #contact_info.user = request.user
            #contact_info.save()
            
            clean_data = contact_info_form.cleaned_data
            Contact_information.objects.update_or_create(
            user = request.user,
            
            defaults={"home_number": clean_data['home_number'],
                      "cell_number": clean_data['cell_number']},
            create_defaults={"user": request.user, 
                            "home_number": clean_data['home_number'],
                            "cell_number": clean_data['cell_number']},
            )

            return redirect('undergraduate')

    context = {
        'contact_info_form': contact_info_form
    }

    return render(request, "main/contact_information.html", context) 


login_required(login_url='login') 
def undergraduate(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    undergraduate_formset = UndergraduateFormSet(queryset=Undergraduate.objects.none(), prefix = 'undergraduate')

    if request.method == 'POST':
        undergraduate_formset = UndergraduateFormSet(request.POST, prefix = 'undergraduate')
        if undergraduate_formset.is_valid():
            for form in undergraduate_formset:
                if form.has_changed():#ignore empty forms
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        undergraduate_info = form.save(commit = False)
                        undergraduate_info.user = request.user
                        undergraduate_info.save()

            return redirect('postgraduate')

    context = {
        'undergraduate_formset': undergraduate_formset
    }

    return render(request, "main/undergraduate.html", context) 


login_required(login_url='login')
def postgraduate(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    postgraduate_formset = PostgraduateFormSet(queryset=Postgraduate.objects.none(), prefix = 'postgraduate')

    if request.method == 'POST':
        postgraduate_formset = PostgraduateFormSet(request.POST, prefix = 'postgraduate')
        if postgraduate_formset.is_valid():
            for form in postgraduate_formset:
                if form.has_changed():#ignore empty forms
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        postgraduate_info = form.save(commit = False)
                        postgraduate_info.user = request.user
                        postgraduate_info.save()

            return redirect('foreign_language')

        else:
            print("not valid")

    context = {
        'postgraduate_formset': postgraduate_formset
    }

    return render(request, "main/postgraduate.html", context) 


login_required(login_url='login') 
def foreign_language(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    foreign_language_formset = ForeignLanguageFormSet(queryset=Foreign_language.objects.none(), prefix = 'foreign_language', 
                                                      form_kwargs={'language_data_list': ('English', 'French', 'German', 'Italian'), #suggestions for language field
                                                                   'level_data_list': ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')}) #suggestions for level field
    
    if request.method == 'POST':
        foreign_language_formset = ForeignLanguageFormSet(request.POST, prefix = 'foreign_language')
        if foreign_language_formset.is_valid():
            for form in foreign_language_formset:
                if form.has_changed():#ignore empty forms
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        foreign_language_info = form.save(commit = False)
                        foreign_language_info.user = request.user
                        foreign_language_info.save()

            return redirect('work_experience')

    context = {
        'foreign_language_formset': foreign_language_formset
    }

    return render(request, "main/foreign_language.html", context) 


login_required(login_url='login') 
def work_experience(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    work_experience_formset = WorkExperienceFormSet(queryset=Work_experience.objects.none(), prefix = 'work_experience')

    if request.method == 'POST':
        work_experience_formset = WorkExperienceFormSet(request.POST, prefix = 'work_experience')
        if work_experience_formset.is_valid():
            for form in work_experience_formset:
                if form.has_changed():#ignore empty forms
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        work_experience_info = form.save(commit = False)
                        work_experience_info.user = request.user
                        work_experience_info.save()

            return redirect('reference_letter')

    context = {
        'work_experience_formset': work_experience_formset
    }

    return render(request, "main/work_experience.html", context) 


login_required(login_url='login') 
def reference_letter(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    reference_letter_formset = ReferenceLetterFormSet(queryset=Reference_letter.objects.none(), prefix = 'reference_letter')

    if request.method == 'POST':
        reference_letter_formset = ReferenceLetterFormSet(request.POST, prefix = 'reference_letter')
        if reference_letter_formset.is_valid():
            for form in reference_letter_formset:
                if form.has_changed():#ignore empty forms
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        reference_letter_info = form.save(commit = False)
                        reference_letter_info.user = request.user
                        reference_letter_info.save()

            return redirect('scholarship')

    context = {
        'reference_letter_formset': reference_letter_formset
    }

    return render(request, "main/reference_letter.html", context) 


login_required(login_url='login') 
def scholarship(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    scholarship_formset = ScholarshipFormSet(queryset=Scholarship.objects.none(), prefix = 'scholarship')

    if request.method == 'POST':
        scholarship_formset = ScholarshipFormSet(request.POST, prefix = 'scholarship')
        if scholarship_formset.is_valid():
            for form in scholarship_formset:
                if form.has_changed():#ignore empty forms
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        scholarship_info = form.save(commit = False)
                        scholarship_info.user = request.user
                        scholarship_info.save()

            return redirect('theses')

    context = {
        'scholarship_formset': scholarship_formset
    }

    return render(request, "main/scholarship.html", context) 


login_required(login_url='login') 
def theses(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    theses_formset = ThesesFormSet(queryset=Theses.objects.none(), prefix = 'theses')

    if request.method == 'POST':
        theses_formset = ThesesFormSet(request.POST, prefix = 'theses')
        if theses_formset.is_valid():
            for form in theses_formset:
                if form.has_changed():#ignore empty forms
                    form_is_deleted = form.cleaned_data['is_deleted']
                    if not form_is_deleted: #ignore deleted (hidden) forms
                        theses_info = form.save(commit = False)
                        theses_info.user = request.user
                        theses_info.save()

            return redirect('my_profile')

    context = {
        'theses_formset': theses_formset
    }

    return render(request, "main/theses.html", context)


login_required(login_url='login') 
def my_profile(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user = request.user
    try:
        contact_information = Contact_information.objects.get(user=user)
    except Contact_information.DoesNotExist:
        contact_information = None

    undergraduate_info = Undergraduate.objects.filter(user=user)
    postgraduate_info = Postgraduate.objects.filter(user=user)
    foreign_language_info = Foreign_language.objects.filter(user=user)
    work_experience_info = Work_experience.objects.filter(user=user)
    reference_letter_info = Reference_letter.objects.filter(user=user)
    scholarship_info = Scholarship.objects.filter(user=user)
    theses_info = Theses.objects.filter(user=user)

    context = { 'user': user, 
               'contact_information': contact_information, 
               'undergraduate_info': undergraduate_info, 
               'postgraduate_info': postgraduate_info, 
               'foreign_language_info': foreign_language_info, 
               'work_experience_info': work_experience_info,
               'reference_letter_info': reference_letter_info,
               'scholarship_info': scholarship_info,
               'theses_info': theses_info}
    return render(request, "main/my_profile.html", context)


login_required(login_url='login')
def update_contact_information(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user = request.user
    contact_info_form = ContactInformationForm(instance = Contact_information.objects.get(user=user))

    if request.method == 'POST':
        contact_info_form = ContactInformationForm(request.POST, instance = Contact_information.objects.get(user=user))
        
        if contact_info_form.is_valid():
            contact_info_form.save()
        
        return redirect('update_undergraduate')

    context = {
        'contact_info_form': contact_info_form
    }

    return render(request, "main/contact_information.html", context)


login_required(login_url='login')
def update_undergraduate(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user = request.user
    undergraduate_formset = UndergraduateFormSet(instance = user, prefix = 'undergraduate')
    
    if request.method == 'POST':
        undergraduate_formset = UndergraduateFormSet(request.POST, instance = user, prefix = 'undergraduate')

        if undergraduate_formset.is_valid():
            for form in undergraduate_formset:
                if form.has_changed():
                    #form.delete() #does not work. Throws error. Can't delete db data using post request data. 
                    #Data needs to be saved to db first (would work if formset can_delete=True) 
                    form.save()
            undergraduate_info = Undergraduate.objects.filter(user=user)
            undergraduate_info_to_be_deleted = undergraduate_info.filter(is_deleted=True)
            for form in undergraduate_info_to_be_deleted:
                form.delete()
        
        return redirect('update_postgraduate')
    
    context = {
        'undergraduate_formset': undergraduate_formset
    }

    return render(request, "main/undergraduate.html", context)
    

login_required(login_url='login')
def update_postgraduate(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user = request.user
    postgraduate_formset = PostgraduateFormSet(instance = user, prefix = 'postgraduate')
    
    if request.method == 'POST':
        postgraduate_formset = PostgraduateFormSet(request.POST, instance = user, prefix = 'postgraduate')

        if postgraduate_formset.is_valid():
            for form in postgraduate_formset:
                if form.has_changed():
                    #form.delete() #does not work. Throws error. Can't delete db data using post request data. 
                    #Data needs to be saved to db first (would work if formset can_delete=True) 
                    form.save()
            postgraduate_info = Postgraduate.objects.filter(user=user)
            postgraduate_info_to_be_deleted = postgraduate_info.filter(is_deleted=True)
            for form in postgraduate_info_to_be_deleted:
                form.delete()
        
        return redirect('update_foreign_language')
    
    context = {
        'postgraduate_formset': postgraduate_formset
    }

    return render(request, "main/postgraduate.html", context) 
    

login_required(login_url='login')
def update_foreign_language(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user = request.user
    foreign_language_formset = ForeignLanguageFormSet(instance = user, prefix = 'foreign_language', 
                                                      form_kwargs={'language_data_list': ('English', 'French', 'German', 'Italian'), #suggestions for language field
                                                                   'level_data_list': ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')}) #suggestions for level field)
    
    if request.method == 'POST':
        foreign_language_formset = ForeignLanguageFormSet(request.POST, instance = user, prefix = 'foreign_language')

        if foreign_language_formset.is_valid():
            for form in foreign_language_formset:
                if form.has_changed():
                    #form.delete() #does not work. Throws error. Can't delete db data using post request data. 
                    #Data needs to be saved to db first (would work if formset can_delete=True) 
                    form.save()
            foreign_language_info = Foreign_language.objects.filter(user=user)
            foreign_language_info_to_be_deleted = foreign_language_info.filter(is_deleted=True)
            for form in foreign_language_info_to_be_deleted:
                form.delete()
        
        return redirect('update_work_experience')
    
    context = {
        'foreign_language_formset': foreign_language_formset
    }

    return render(request, "main/foreign_language.html", context) 
    

login_required(login_url='login')
def update_work_experience(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user = request.user
    work_experience_formset = WorkExperienceFormSet(instance = user, prefix = 'work_experience')
    
    if request.method == 'POST':
        work_experience_formset = WorkExperienceFormSet(request.POST, instance = user, prefix = 'work_experience')

        if work_experience_formset.is_valid():
            for form in work_experience_formset:
                if form.has_changed():
                    #form.delete() #does not work. Throws error. Can't delete db data using post request data. 
                    #Data needs to be saved to db first (would work if formset can_delete=True) 
                    form.save()
            work_experience_info = Work_experience.objects.filter(user=user)
            work_experience_info_to_be_deleted = work_experience_info.filter(is_deleted=True)
            for form in work_experience_info_to_be_deleted:
                form.delete()
        
        return redirect('update_reference_letter')
    
    context = {
        'work_experience_formset': work_experience_formset
    }

    return render(request, "main/work_experience.html", context) 
    

login_required(login_url='login')
def update_reference_letter(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user = request.user
    reference_letter_formset = ReferenceLetterFormSet(instance = user, prefix = 'reference_letter')
    
    if request.method == 'POST':
        reference_letter_formset = ReferenceLetterFormSet(request.POST, instance = user, prefix = 'reference_letter')

        if reference_letter_formset.is_valid():
            for form in reference_letter_formset:
                if form.has_changed():
                    #form.delete() #does not work. Throws error. Can't delete db data using post request data. 
                    #Data needs to be saved to db first (would work if formset can_delete=True) 
                    form.save()
            reference_letter_info = Reference_letter.objects.filter(user=user)
            reference_letter_info_to_be_deleted = reference_letter_info.filter(is_deleted=True)
            for form in reference_letter_info_to_be_deleted:
                form.delete()
        
        return redirect('update_scholarship')

    context = {
        'reference_letter_formset': reference_letter_formset
    }

    return render(request, "main/reference_letter.html", context)  


login_required(login_url='login')
def update_scholarship(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    user = request.user
    scholarship_formset = ScholarshipFormSet(instance = user, prefix = 'scholarship')
    
    if request.method == 'POST':
        scholarship_formset = ScholarshipFormSet(request.POST, instance = user, prefix = 'scholarship')

        if scholarship_formset.is_valid():
            for form in scholarship_formset:
                if form.has_changed():
                    #form.delete() #does not work. Throws error. Can't delete db data using post request data. 
                    #Data needs to be saved to db first (would work if formset can_delete=True) 
                    form.save()
            scholarship_info = Scholarship.objects.filter(user=user)
            scholarship_info_to_be_deleted = scholarship_info.filter(is_deleted=True)
            for form in scholarship_info_to_be_deleted:
                form.delete()
        
        return redirect('update_theses')
    
    context = {
        'scholarship_formset': scholarship_formset
    }

    return render(request, "main/scholarship.html", context)


login_required(login_url='login')
def update_theses(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home') 
    
    user = request.user
    theses_formset = ThesesFormSet(instance = user, prefix = 'theses')

    if request.method == 'POST':
        theses_formset = ThesesFormSet(request.POST, instance = user, prefix = 'theses')

        if theses_formset.is_valid():
            for form in theses_formset:
                if form.has_changed():
                    #form.delete() #does not work. Throws error. Can't delete db data using post request data. 
                    #Data needs to be saved to db first (would work if formset can_delete=True) 
                    form.save()
            theses_info = Theses.objects.filter(user=user)
            theses_info_to_be_deleted = theses_info.filter(is_deleted=True)
            for form in theses_info_to_be_deleted:
                form.delete()
        
        return redirect('my_profile')  

    context = {
        'theses_formset': theses_formset
    }

    return render(request, "main/theses.html", context)             


login_required(login_url='login') 
def choose_master(request):
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    master_form = MasterForm()

    if request.method == 'POST':
        master_form = MasterForm(request.POST)
        if master_form.is_valid():
            application = Application(user=request.user, master= master_form.cleaned_data['name'])
            application.save()

            return redirect('choose_orientation', application.id)
        else:
            print(master_form.errors)
    
    context = {'master_form': master_form

    }

    return render(request, "main/choose_master.html", context)


login_required(login_url='login') 
def choose_orientation(request, pk): #view used for both create and update
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    application = Application.objects.get(id=pk)

    if application.is_validated:
        return redirect('home') #can't update a validated application

    master = application.master
    orientation_form = OrientationForm(master=master)

    if request.method == 'POST':
        orientation_form = OrientationForm(master=master, data=request.POST)
        if orientation_form.is_valid():
            application.orientation = orientation_form.cleaned_data['name']
            application.save()

            request.user.has_applied = True
            request.user.save()  

            return redirect('my_applications')
        else:
            print(orientation_form.errors)
    
    context = {'orientation_form': orientation_form

    }

    return render(request, "main/choose_orientation.html", context)


login_required(login_url='login')
def update_master(request, pk): #change an application that has already been created
    if request.user.groups.filter(name='Grammateia').exists():
        return redirect('home')
    
    application = Application.objects.get(id=pk)

    if application.is_validated:
        return redirect('home') #should not be able to update a validated application
    
    print(application.master)
    #user = User.objects.get(application=application)
    print(Master.objects.get(name=application.master))

    master_form = MasterForm()

    if request.method == 'POST':
        master_form = MasterForm(request.POST)
        if master_form.is_valid():
            application.master = master_form.cleaned_data['name']
            application.save()

            return redirect('choose_orientation', application.id)
        else:
            print(master_form.errors)

    context = {'master_form': master_form

    }

    return render(request, "main/choose_master.html", context)








    



      
    