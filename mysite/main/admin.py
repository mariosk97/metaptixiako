from django.contrib import admin
from .models import Application, User, Contact_information

# Register your models here.


admin.site.register(User)
admin.site.register(Application)
admin.site.register(Contact_information)


