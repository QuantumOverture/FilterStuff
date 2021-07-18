from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','password1','password2']
        

class WordDeleteForm(forms.Form):
    def __init__(self, OptionTexts, *args, **kwargs):
        self.base_fields['Options'].choices = OptionTexts
        super(WordDeleteForm, self).__init__(*args, **kwargs)

    Options = forms.ChoiceField(choices=(),widget=forms.RadioSelect,required=False,label="Delete Word:")

class WordEntryForm(forms.Form):
    NewWordField = forms.CharField(widget=forms.TextInput,required=False,label="Add Word:")
   

class RedditSearch(forms.Form):
    Subreddit = forms.CharField(widget=forms.TextInput,required=False)