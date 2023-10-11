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
        null=True
    )

    class Μilitary_service(models.TextChoices):
        completed = "completed"
        not_completed = "not completed" 

    military_service = models.CharField(
        max_length=13,
        choices=Μilitary_service.choices,
        null=True
    )
    
    date_of_birth = models.DateField(null=True) # user should be able to choose. Maybe try date input widget
    place_of_birth = models.CharField(max_length=150, null=True)
    prefecture = models.CharField(max_length=150, null=True) #νομός
    country = models.CharField(max_length=150, null=True)

    def validate_amka(amka): #amka must be eleven digits
        if not (amka.isdigit() and len(amka) == 11):    
            raise ValidationError('amka must be 11 digits')

    amka = models.CharField(max_length=11, validators=[validate_amka], null = True)

    def validate_afm(afm): #amka must be eleven digits
        if not (afm.isdigit() and len(afm) == 9):    
            raise ValidationError('afm must be 9 digits')

    afm = models.CharField(max_length=9, validators=[validate_afm], null = True)     
   
    
    #doy
    #id_number = models.CharField(max_length=150, null=True)

class Application(models.Model):
    #readonly_fields = ["created"] #to show created time in admin. Does not work.
    
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True) #change null=True
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) #time created should be when has_applied=True
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.user) #maybe change to something else later, this is what is shown in admin
    

class Contact_information(models.Model):   
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True) 
    
    def validate_number(number): #amka must be eleven digits
        if not (number.isdigit() and len(number) == 10):    
            raise ValidationError('number must be 10 digits')

    home_number = models.CharField(max_length=10, validators=[validate_number], null = True) 
    cell_number = models.CharField(max_length=10, validators=[validate_number], null = True) 

    def __str__(self):
        return str(self.user) #this is shown in admin


        
            
        

