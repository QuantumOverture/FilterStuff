from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',views.RegisterView,name="RegisterView"),
    path('login/',auth_views.LoginView.as_view(template_name="MainApp/login.html"),name="LoginView"),
    path('logout/',auth_views.LogoutView.as_view(template_name="MainApp/logout.html"),name="LogoutView"),
    path('u/<str:UserName>',views.UserView,name="UserView"),
    path('u/',views.UserViewRedirect,name="UserViewRedirect"),
    path('',views.HomePage,name="HomePage"),
    
]