from django.contrib.auth.models import User
from django.db import models


class ComputerQuiz(models.Model):
    question = models.TextField(default="", max_length=200)
    option1 = models.CharField(default = "", max_length=50)
    option2 = models.CharField(default = "", max_length=50)
    option3 = models.CharField(default = "", max_length=50)
    option4 = models.CharField(default = "", max_length=50)
    correct_ans = models.CharField(default= "", max_length=50)

class ScienceQuiz(models.Model):
    question = models.TextField(default="", max_length=200)
    option1 = models.CharField(default = "", max_length=50)
    option2 = models.CharField(default = "", max_length=50)
    option3 = models.CharField(default = "", max_length=50)
    option4 = models.CharField(default = "", max_length=50)
    correct_ans = models.CharField(default= "", max_length=50)

class GKQuiz(models.Model):
    question = models.TextField(default="", max_length=200)
    option1 = models.CharField(default = "", max_length=50)
    option2 = models.CharField(default = "", max_length=50)
    option3 = models.CharField(default = "", max_length=50)
    option4 = models.CharField(default = "", max_length=50)
    correct_ans = models.CharField(default= "", max_length=50)

class UserTestData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    computer_responses = models.TextField(default = "")
    science_responses = models.TextField(default = "")
    gk_responses = models.TextField(default = "")
    computer_status = models.BooleanField(default = False)
    science_status = models.BooleanField(default = False)
    gk_status = models.BooleanField(default = False)

    def __str__(self):
        return self.user.first_name + "(" + self.user.username + ")"
    