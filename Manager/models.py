from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField

# Create your models here.

class PM(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Event(models.Model):
    drive_name = models.CharField(max_length=100)
    last_date = models.DateField()
    role = models.CharField(max_length=100)
    req =  models.CharField(max_length=400)
    ctc =  models.CharField(max_length=20)
    passouts =  models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    stu_applied = models.CharField(max_length=400,null=True)
