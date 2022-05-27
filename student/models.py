from datetime import datetime
from distutils.command.upload import upload
from operator import contains
import os
from pyexpat import model
from tkinter import CASCADE
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


def path_and_rename(instance, filename):
    print(filename, instance)
    if ".pdf" in filename:
        upload_to = 'resume'
    else:
        upload_to = 'profile'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.PRN, ext)
    else:
        # set filename as random string 
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def offerletterUpload(instance, filename):
    upload_to = 'offerletter'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        ct = datetime.datetime.now()
        filename = '{}.{}'.format(instance.PRN+"_"+str(int(ct.timestamp())), ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


# Create your models here.
class Admin(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)


class Student(models.Model):
    email = models.CharField(max_length=100)
    verified = models.BooleanField()
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    extra_curriculam = models.CharField(max_length=400, null=True)
    profile = models.FileField(upload_to=path_and_rename, null=True, default='avtar.png')
    resume = models.FileField(upload_to=path_and_rename, null=True)
    PlacementStatus = models.BooleanField(null=True)
    Department = models.CharField(max_length=100,null=True)


class StudentEducation(models.Model):
    # BTech
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ug_stream = models.CharField(max_length=100)
    ug_admission = models.IntegerField(null=True)
    ug_passout = models.IntegerField()
    gap = models.BooleanField(default=False)
    
    # Percentage
    ug_backlog  = models.PositiveIntegerField(default=0)
    ug_fy_sem1 = models.FloatField(null=True)
    ug_sy_sem1 = models.FloatField(null=True)
    ug_ty_sem1 = models.FloatField(null=True)
    ug_be_sem1 = models.FloatField(null=True)
    ug_fy_sem2 = models.FloatField(null=True)
    ug_sy_sem2 = models.FloatField(null=True)
    ug_ty_sem2 = models.FloatField(null=True)
    ug_be_sem2 = models.FloatField(null=True)
    ug_total = models.FloatField(null=True)
    
    # Atkt
    ug_fy_atkt = models.IntegerField(null=True)
    ug_sy_atkt = models.IntegerField(null=True)
    ug_ty_atkt = models.IntegerField(null=True)
    ug_be_atkt = models.IntegerField(null=True)
    # gap
    ug_fy_gap = models.IntegerField(null=True)
    ug_sy_gap = models.IntegerField(null=True)
    ug_ty_gap = models.IntegerField(null=True)
    ug_be_gap = models.IntegerField(null=True)

    # Diploma
    diploma_college_name = models.CharField(max_length=100, null=True)
    diploma_stream = models.CharField(max_length=50, null=True)
    diploma_passout = models.IntegerField(null=True)

    diploma_fy = models.FloatField(null=True)
    diploma_sy = models.FloatField(null=True)
    diploma_ty = models.FloatField(null=True)
    diploma_total = models.FloatField(null=True,default=0)

    # HSC
    hsc_college_name = models.CharField(max_length=100, null=True)
    hsc_marks = models.FloatField(null=True,default=0)
    hsc_passout = models.IntegerField(null=True)

    # ssc
    school_name = models.CharField(max_length=100)
    school_marks = models.FloatField(default=0)
    school_passout = models.IntegerField()


class Placementinfo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    CompanyName = models.CharField(max_length=100)
    Role = models.CharField(max_length=50)
    JoinDate = models.DateField()
    CTC = models.IntegerField()
    Offerletter = models.FileField(upload_to=offerletterUpload, null=True)
    HRname = models.CharField(max_length=100)


class Cocurriclar(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    CompanyName = models.CharField(max_length=100)
    Description = models.CharField(max_length=200)

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
