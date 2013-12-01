from django.contrib import admin
from django import forms
from django.contrib.auth.models import User

from sample.models import (Doctor, Worker, Patient, SpecialtyType, TimeSlot, Case, Comment, CommentGroup,
        Scan)

class searchDoctor(admin.ModelAdmin):
    list_display = ['user_first_name', 'user_last_name', 'get_some_value']
    search_fields = ['user__first_name', 'user__last_name', 
                     'specialties__name']

class searchWorker(admin.ModelAdmin):
    list_display = ['user_first_name', 'user_last_name']
    search_fields = ['user__first_name', 'user__last_name']

class searchPatient(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

class searchSpeciality(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']

class searchTimeslot(admin.ModelAdmin):
    search_fields = ['start_time', 'end_time']

class searchCase(admin.ModelAdmin):
    search_fields = ['id']
    list_display = ['id']

class searchComment(admin.ModelAdmin):
    search_fields = ['text']
    list_display = ['text']

class searchScan(admin.ModelAdmin):
    search_fields = ['patient', 'comments']

admin.site.register(Doctor, searchDoctor)
admin.site.register(Worker, searchWorker)
admin.site.register(Patient, searchPatient)
admin.site.register(SpecialtyType, searchSpeciality)
admin.site.register(TimeSlot, searchTimeslot)
admin.site.register(Case, searchCase)
admin.site.register(Comment, searchComment)
admin.site.register(CommentGroup)
admin.site.register(Scan, searchScan)
