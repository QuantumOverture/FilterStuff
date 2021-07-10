from django.shortcuts import render,HttpResponse

def HomePage(request):
    return HttpResponse("<h1>HomePage</h1>")
    
def UserView(request,UserName):
    return HttpResponse("<h1>{}</h1>".format(UserName))
