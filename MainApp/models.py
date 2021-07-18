from django.db import models
from django.contrib.auth.models import User

class UserListWord(models.Model):
    Word = models.CharField(max_length=100)
    UserName = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "words")