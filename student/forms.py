

from django import forms
from .models import *
from django.forms import ModelForm


class ImageUpload(ModelForm):
    class Meta():
        model = Student
        fields = {
            'profile'
        }
        widget = {'profile': forms.FileInput(
            attrs={'id': "OpenImgUpload", "type": "image"})}


class ResumeUpload(ModelForm):
    class Meta():
        model = Student
        fields = {
            'resume'
        }
        widgets = {
            'resume':forms.FileInput(
                attrs= {
                    'name':'uploadResume',
                    'class' : 'uploadResume'
                }
            )
        }


class OfferLetterUpload(ModelForm):
    # CompanyName = forms.CharField(max_length=100)
    # Role = forms.CharField(max_length=50)
    # JoinDate = forms.DateField()
    # CTC = forms.IntegerField()
    # Offerletter = forms.FileField()
    # HRname = forms.CharField(max_length=100)

    class Meta():
        model = Placementinfo
        fields = {
            'CompanyName',
            'Role',
            'HRname',
            'JoinDate',
            'CTC',
            'Offerletter'
        }
        
 

        widgets = {
            'JoinDate':forms.DateInput(
                attrs= {
                    'type':'date'
                }
            )
        }
