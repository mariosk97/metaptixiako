from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.core.exceptions import ValidationError
# Create your models here.

class User(AbstractUser):
    has_applied = models.BooleanField(default=False)
    fathers_name = models.CharField(max_length=150, null=True)
    mothers_name = models.CharField(max_length=150, null=True)
   
    class Sex(models.TextChoices):
        male = "male"
        female = "female" 

    sex = models.CharField(
        max_length=6,
        choices=Sex.choices,
        null=True
    )

    class Marital_status(models.TextChoices):
        married = "married"
        unmarried = "unmarried" 

    marital_status = models.CharField(
        max_length=9,
        choices=Marital_status.choices,
        null=True,
        blank=True
    )

    class Μilitary_service(models.TextChoices):
        completed = "completed"
        not_completed = "not completed" 

    military_service = models.CharField(
        max_length=13,
        choices=Μilitary_service.choices,
        null=True,
        blank=True
    )
    
    date_of_birth = models.DateField(null=True) 
    place_of_birth = models.CharField(max_length=150, null=True)
    prefecture = models.CharField(max_length=150, null=True) #νομός
    country = models.CharField(max_length=150, null=True)

    def validate_amka(amka): #amka must be eleven digits
        if not (amka.isdigit() and len(amka) == 11):    
            raise ValidationError('amka must be 11 digits')

    amka = models.CharField(max_length=11, validators=[validate_amka], null = True)

    def validate_afm(afm): #afm must be 9 digits
        if not (afm.isdigit() and len(afm) == 9):    
            raise ValidationError('afm must be 9 digits')

    afm = models.CharField(max_length=9, validators=[validate_afm], null = True)     
   

class Master(models.Model):
    name = models.CharField(max_length=150, null=True)
      
    def __str__(self):
        return str(self.name) 
    

class Orientation(models.Model):
    name = models.CharField(max_length=150, null=True)
    master = models.ForeignKey(Master,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)


class Application(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) #change null=True
    master = models.ForeignKey(Master,on_delete=models.CASCADE, null=True)
    orientation = models.ForeignKey(Orientation,on_delete=models.CASCADE, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 
    is_validated = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_withdrawn = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-updated', '-created']
        permissions = [
            ("validate_application", "Can validate an application"),
            ("accept_application", "Can accept an application")
        ]

    def __str__(self):
        return str(self.user) #this is shown in admin       
    

class Contact_information(models.Model):   
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True) 
    
    def validate_number(number): #must be ten digits
        if not (number.isdigit() and len(number) == 10):    
            raise ValidationError('number must be 10 digits')

    home_number = models.CharField(max_length=10, validators=[validate_number], null = True) 
    cell_number = models.CharField(max_length=10, validators=[validate_number], null = True) 

    def __str__(self):
        return str(self.user) #this is shown in admin
    

class Foreign_language(models.Model):   
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)   
    language = models.CharField(max_length=150, null=True, blank=True)
    level = models.CharField(max_length=150, null=True, blank=True)
    degree = models.CharField(max_length=150, null=True, blank=True)
    grade = models.FloatField(null=True, blank=True)
    acquisition_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="languages", null=True, blank=True)
    is_deleted = models.BooleanField(default = False) #true when the user wants to remove the form

    def __str__(self):
        return str(self.user) #this is shown in admin  
    

class Work_experience(models.Model):   
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)   
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank = True)
    company = models.CharField(max_length=150, null=True, blank=True)
    position = models.CharField(max_length=150, null=True, blank=True)
    is_deleted = models.BooleanField(default = False) #true when the user wants to remove the form

    def __str__(self):
        return str(self.user) #this is shown in admin    


class Reference_letter(models.Model):   
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    full_name = models.CharField(max_length=150, null=True, blank=True)  
    position = models.CharField(max_length=150, null=True, blank=True)
    organization = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_deleted = models.BooleanField(default = False) #true when the user wants to remove the form
    
    def __str__(self):
        return str(self.user) #this is shown in admin     


class Scholarship(models.Model):   
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    description = models.CharField(max_length=150, null=True, blank=True)  
    acquisition_date = models.DateField(null=True, blank = True)
    educational_institution = models.CharField(max_length=150, null=True, blank=True) 
    is_deleted = models.BooleanField(default = False) #true when the user wants to remove the form
    
    def __str__(self):
        return str(self.user) #this is shown in admin  


class Theses(models.Model): #Diploma, undergraduate and postgraduate theses   
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    title = models.CharField(max_length=150, null=True, blank = True)
    supervisor = models.CharField(max_length=150, null=True, blank = True)
    grade = models.FloatField(null=True, blank = True)
    is_deleted = models.BooleanField(default = False) #true when the user wants to remove the form
     
    def __str__(self):
        return str(self.user) #this is shown in admin  


class Studies(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    univercity = models.CharField(max_length=150, null=True, blank = True) #required field. Code in clean function in StudyForm. Can't remove blank=true because of is_deleted
    department = models.CharField(max_length=150, null=True, blank = True) #required field. Code in clean function in StudyForm. Can't remove blank=true because of is_deleted
    degree_title = models.CharField(max_length=150, null=True, blank = True)
    grade = models.FloatField(null=True, blank = True)
    photo = models.ImageField(upload_to="studies", null=True, blank = True)
    is_deleted = models.BooleanField(default = False) #true when the user wants to remove the form

    class Meta:
        abstract = True #Base class for other models

      
class Undergraduate(Studies):   

    def __str__(self):
        return str(self.user) 
    

class Postgraduate(Studies):   

    def __str__(self):
        return str(self.user)     
        
            
        

