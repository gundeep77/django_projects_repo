from django.db import models
from django.contrib.auth.models import User
import datetime

class NewLoan(models.Model):
    fname = models.CharField(max_length=50, default = "")
    amount = models.IntegerField(default = 0)
    tenure = models.IntegerField(default = 0)
    comments = models.CharField(max_length = 150, default = "")
    apply_date = models.DateField(default = datetime.date.today())
    
    def __str__(self):
        return self.fname
        

class RejectedLoan(models.Model):
    pass

class ApprovedLoan(models.Model):
    pass