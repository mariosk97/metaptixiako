from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_page, name="register"),
    path("", views.home, name="home"),
    path("applications/", views.applications, name="all_applications"), 
    path("applications/<str:pk>/", views.application, name="application"),
    path("create-application/", views.create_application, name="create_application"),
    path("update-master/<str:pk>/", views.update_master, name="update_master"),  
    path("delete-application/<str:pk>/", views.delete_application, name="delete_application"),
    path("validate-application/<str:pk>/", views.validate_application, name="validate_application"),
    path("accept-application/<str:pk>/", views.accept_application, name="accept_application"),
    path("my-applications/", views.my_applications, name="my_applications"),  

    path("user-information/", views.user_information, name="user_information"),
    path("contact-information/", views.contact_information, name="contact_information"),
    path("undergraduate/", views.undergraduate, name="undergraduate"),
    path("postgraduate/", views.postgraduate, name="postgraduate"),
    path("foreign-language/", views.foreign_language, name="foreign_language"),
    path("work-experience/", views.work_experience, name="work_experience"),
    path("reference-letter/", views.reference_letter, name="reference_letter"),
    path("scholarship/", views.scholarship, name="scholarship"),
    path("theses/", views.theses, name="theses"),
    path("my-profile/", views.my_profile, name="my_profile"),
    path("choose-master/", views.choose_master, name="choose_master"),
    path("choose-orientation/<str:pk>/", views.choose_orientation, name="choose_orientation"),
    
    

]