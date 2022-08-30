from django.contrib import admin

# Register your models here.

from .models import Application, User

admin.site.register(User)
admin.site.register(Application)
