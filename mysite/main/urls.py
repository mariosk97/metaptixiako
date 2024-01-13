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
    path("update-application/<str:pk>/", views.update_application, name="update_application"),  
    path("delete-application/<str:pk>/", views.delete_application, name="delete_application"),
    path("validate-application/<str:pk>/", views.validate_application, name="validate_application"),
    path("accept-application/<str:pk>/", views.accept_application, name="accept_application"),
    path("my_application/", views.my_application, name="my_application"),  
    

]