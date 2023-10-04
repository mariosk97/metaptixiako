from django.contrib import admin
from .models import Application, User

# Register your models here.


admin.site.register(User)
admin.site.register(Application)


