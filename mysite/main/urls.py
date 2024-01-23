from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", views.home, name="home"),

    #CRUD for user
    path("my-profile/", views.my_profile, name="my_profile"),

    path("register/", views.register_page, name="register"),
    path("user-information/", views.user_information, name="user_information"),
    path("contact-information/", views.contact_information, name="contact_information"),
    path("undergraduate/", views.undergraduate, name="undergraduate"),
    path("postgraduate/", views.postgraduate, name="postgraduate"),
    path("foreign-language/", views.foreign_language, name="foreign_language"),
    path("work-experience/", views.work_experience, name="work_experience"),
    path("reference-letter/", views.reference_letter, name="reference_letter"),
    path("scholarship/", views.scholarship, name="scholarship"),
    path("theses/", views.theses, name="theses"),

    path("update-user-information/", views.user_information, name="user_information"),
    path("update-contact-information/", views.update_contact_information, name="update_contact_information"),
    path("update-undergraduate/", views.update_undergraduate, name="update_undergraduate"),
    path("update-postgraduate/", views.update_postgraduate, name="update_postgraduate"),
    path("update-foreign-language/", views.update_foreign_language, name="update_foreign_language"),
    path("update-work-experience/", views.update_work_experience, name="update_work_experience"),
    path("update-reference-letter/", views.update_reference_letter, name="update_reference_letter"),
    path("update-scholarship/", views.update_scholarship, name="update_scholarship"),
    path("update-theses/", views.update_theses, name="update_theses"),
      
    #CRUD for application 
    path("choose-master/", views.choose_master, name="choose_master"),
    path("choose-orientation/<str:pk>/", views.choose_orientation, name="choose_orientation"),

    path("update-master/<str:pk>/", views.update_master, name="update_master"),

    path("delete-application/<str:pk>/", views.delete_application, name="delete_application"),

    path("my-applications/", views.my_applications, name="my_applications"),

    path("create-application/", views.create_application, name="create_application"), #not used??

    #Grammateia
    path("applications/", views.applications, name="all_applications"), 
    path("applications/<str:pk>/", views.application, name="application"),
    path("validate-application/<str:pk>/", views.validate_application, name="validate_application"),
    path("accept-application/<str:pk>/", views.accept_application, name="accept_application"),
    
]