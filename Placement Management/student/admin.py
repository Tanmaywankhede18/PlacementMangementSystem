from django.contrib import admin
from .models import Admin, Student, PM, Event
# Register your models here.
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(PM)
admin.site.register(Event)