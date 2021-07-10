from django.shortcuts import render,HttpResponse,redirect
from .forms import UserRegisterForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def HomePage(request):
	return render(request,"MainApp/index.html")

@login_required    
def UserView(request,UserName):

    if UserName != request.user.username:
        return redirect("UserView",UserName = request.user.username)
    return HttpResponse("<h1>{}</h1>".format(UserName))
    
@login_required 
def UserViewRedirect(request):
    return redirect("UserView",UserName = request.user.username)

def RegisterView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('LoginView')
    else:
        form = UserRegisterForm()
    return render(request,"MainApp/register.html",{'form':form})