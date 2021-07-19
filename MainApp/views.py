from django.shortcuts import render,HttpResponse,redirect
from .forms import UserRegisterForm,WordEntryForm,WordDeleteForm,RedditSearch
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from MainApp.models import UserListWord
import praw
from praw.models import MoreComments
import json

def HomePage(request):
	return render(request,"MainApp/index.html")

@login_required    
def UserView(request,UserName):
    if UserName != request.user.username:
        return redirect("UserView",UserName = request.user.username)
     
     
    WordEntryFormData = WordEntryForm()
    SubredditTitle = ""    
    WordOptions = UserListWord.objects.filter(UserName=User.objects.filter(username=request.user.username)[0])
    WordList = []
    for Val in range(len(WordOptions)):
        WordList.append((WordOptions[Val].Word,WordOptions[Val].Word))
    WordDeleteFormData = WordDeleteForm(WordList)
    SelectedSubredditData = []
    RedditSearchData = RedditSearch()
        
    if request.method == "POST":     
        if "AddWord" in request.POST:
            form = WordEntryForm(request.POST)
            if form.is_valid():
                NewWord = form.cleaned_data["NewWordField"]
                NewWordModel = UserListWord(Word = NewWord, UserName = request.user)
                NewWordModel.save()
            return redirect("UserView",UserName = request.user.username)
            
        elif "DeleteWord" in request.POST:
            
            form = WordDeleteForm(request.POST)
            try:
                DelWord = request.POST["Options"]
                UserListWord.objects.filter(Word = DelWord, UserName = request.user).delete()
            except:
                pass
            
            return redirect("UserView",UserName = request.user.username)
        elif "Search" in request.POST:
            form = RedditSearch(request.POST)
            if form.is_valid():
                Subreddit = form.cleaned_data["Subreddit"]
                SubredditTitle = Subreddit
                JSONCred = open("RedditApiCreds.json","r")
                JSONCredData = json.load(JSONCred)
                JSONCred.close()
                
                
                RedditCrawl = praw.Reddit(
                    client_id= JSONCredData["client_id"],
                    client_secret= JSONCredData["client_secret"],
                    user_agent= JSONCredData["user_agent"],
                )
                
                try:
                    for submission in RedditCrawl.subreddit(Subreddit).hot(limit=13):
                        Text = submission.selftext
                        Title = submission.title
                        URL = submission.url
                        InvalidFlag = False

                        for Word in WordList:
                            WordMatch = Word[0].lower()
                            if WordMatch in Text.lower() or WordMatch in Title.lower():
                                InvalidFlag = True
                                break
                            else:
                                continue
                        
                        
                        if not InvalidFlag:
                            SelectedSubredditData.append({"title":Title,
                            "description":Text,
                            "url":URL})
                           
                except:
                    SelectedSubredditData.append({"title":"Invalid Subreddit","description":""})
        else:
            return redirect('HomePage')
            
             
    return render(request,"MainApp/user.html",{'UserName':UserName,
    "WordEntryForm":WordEntryFormData,
    "WordDeleteForm":WordDeleteFormData,
    "RedditSearch":RedditSearchData,
    "SubredditData":SelectedSubredditData,
    "SubredditTitle":SubredditTitle})
       
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