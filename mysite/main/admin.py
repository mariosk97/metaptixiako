from django.contrib import admin
from .models import Application, User, Contact_information, Foreign_language, Work_experience, Reference_letter, Theses, Scholarship, Undergraduate, Postgraduate

# Register your models here.


admin.site.register(User)
admin.site.register(Application)
admin.site.register(Contact_information)
admin.site.register(Foreign_language)
admin.site.register(Work_experience)
admin.site.register(Reference_letter)
admin.site.register(Theses)
admin.site.register(Scholarship)
admin.site.register(Undergraduate)
admin.site.register(Postgraduate)


