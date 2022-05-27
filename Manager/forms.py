from django import forms
from .models import *
from django.forms import ModelForm


class EventForm(ModelForm):
    class Meta():
        model = Event
        fields = {
            'drive_name',
            'last_date',
            'role',
            'req',
            'ctc',
            'passouts',
            'link',
        }
        field_order = [
            'drive_name',
            'last_date',
            'role',
            'req',
            'ctc',
            'passouts',
            'link', 
            ]
