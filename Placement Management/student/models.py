from operator import mod
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField

# Create your models here.
class Admin(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    
class Student(models.Model):
    email = models.CharField(max_length=100)
    roll = models.CharField(max_length=10,default='student')
    verified = models.BooleanField();
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    PRN = models.CharField(max_length=100)
    ug = models.CharField(max_length=100)
    ug_marks = models.CharField(max_length=5)
    ug_backlogs = models.CharField(max_length=5)
    ug_stream = models.CharField(max_length=50)
    ug_passout = models.CharField(max_length=5)
    diploma = models.CharField(max_length=100, null=True)
    diploma_marks= models.CharField(max_length=5,null=True)
    diploma_stream = models.CharField(max_length=50)
    hsc = models.CharField(max_length=100,null=True)
    hsc_marks = models.CharField(max_length=100,null=True)
    diploma_passout = models.CharField(max_length=5)
    school = models.CharField(max_length=100)
    school_marks= models.CharField(max_length=5)
    school_passout = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    extra_curriculam = models.JSONField(null=True)
     



class PM(models.Model):
    roll = models.CharField(max_length=10,default='pm')
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Event(models.Model):
    drive_name = models.CharField(max_length=100)
    last_date = models.DateField()
    roll = models.CharField(max_length=100)
    req =  models.CharField(max_length=400)
    ctc =  models.CharField(max_length=20)
    passouts =  models.CharField(max_length=100)
    link = models.CharField(max_length=200)