from django.urls import path
from . import views
urlpatterns = [
    path('u/<str:UserName>',views.UserView,name="UserView"),
    path('',views.HomePage,name="HomePage"),
    
]