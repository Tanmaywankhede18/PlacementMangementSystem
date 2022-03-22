from operator import mod
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
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
    # ug = models.CharField(max_length=100)
    # ug_marks = models.CharField(max_length=5)
    # ug_backlogs = models.CharField(max_length=5)
    # ug_stream = models.CharField(max_length=50)
    # ug_passout = models.CharField(max_length=5)
    # diploma = models.CharField(max_length=100, null=True)
    # diploma_marks= models.CharField(max_length=5,null=True)
    # diploma_stream = models.CharField(max_length=50)
    # hsc = models.CharField(max_length=100,null=True)
    # hsc_marks = models.CharField(max_length=100,null=True)
    # diploma_passout = models.CharField(max_length=5)
    # school = models.CharField(max_length=100)
    # school_marks= models.CharField(max_length=5)
    # school_passout = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    extra_curriculam = models.JSONField(null=True)
     

class StudentEducation(models.Model):
    #BTech
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    ug_stream = models.CharField(max_length=100)
    ug_admmision = models.IntegerField(null=True)
    ug_passout = models.IntegerField()
    #Percentage 
    ug_fy_sem1 = models.IntegerField(null=True)
    ug_sy_sem1 = models.IntegerField(null=True)
    ug_ty_sem1 = models.IntegerField(null=True)
    ug_be_sem1 = models.IntegerField(null=True)
    ug_fy_sem2 = models.IntegerField(null=True)
    ug_sy_sem2 = models.IntegerField(null=True)
    ug_ty_sem2 = models.IntegerField(null=True)
    ug_be_sem2 = models.IntegerField(null=True)
    #Atkt
    ug_fy_atkt = models.IntegerField(null=True)
    ug_sy_atkt = models.IntegerField(null=True)
    ug_ty_atkt = models.IntegerField(null=True)
    ug_be_atkt = models.IntegerField(null=True)
    #gap
    ug_fy_gap  = models.IntegerField(null=True)
    ug_sy_gap  = models.IntegerField(null=True)
    ug_ty_gap  = models.IntegerField(null=True)
    ug_be_gap  = models.IntegerField(null=True)


    #Diploma
    diploma_college_name = models.CharField(max_length=100,null=True)
    diploma_stream = models.CharField(max_length=50,null=True)
    diploma_passout = models.IntegerField(null=True)

    diploma_fy = models.IntegerField(null=True)
    diploma_sy = models.IntegerField(null=True)
    diploma_ty = models.IntegerField(null=True)
    diploma_total = models.IntegerField(null=True)

    #HSC 
    hsc_college_name = models.CharField(max_length=100,null=True)
    hsc_marks = models.IntegerField(null=True)
    hsc_passout = models.IntegerField(null=True)

    #ssc
    school_name = models.CharField(max_length=100)
    school_marks = models.IntegerField()
    school_passout = models.IntegerField()
       

# class PM(models.Model):
#     fullname = models.CharField(max_length=100)
#     email = models.CharField(max_length=30)
#     mobile = models.CharField(max_length=10)
#     department = models.CharField(max_length=100)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)

# class Event(models.Model):
#     drive_name = models.CharField(max_length=100)
#     last_date = models.DateField()
#     roll = models.CharField(max_length=100)
#     req =  models.CharField(max_length=400)
#     ctc =  models.CharField(max_length=20)
#     passouts =  models.CharField(max_length=100)
#     link = models.CharField(max_length=200)