from django.contrib import admin

from sample.models import (Doctor, Worker, Patient, Measurement,
        MeasurementType, SpecialtyType, TimeSlot, Case, Scan, Annotation)

def first_name(self):
    return self.user.first_name

def last_name(self):
    return self.user.last_name

class searchUser(admin.ModelAdmin):
    list_display = ['user_first_name', 'user_last_name']
    search_fields = ['user__first_name', 'user__last_name']
    
class searchPatient(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    
class searchMType(admin.ModelAdmin):
    search_fields = ['name']
    
class searchMeasurement(admin.ModelAdmin):
    search_fields = ['worker', 'patient', 'measurement_type']
    
class searchSpeciality(admin.ModelAdmin):
    search_fields = ['name']

class searchTimeslot(admin.ModelAdmin):
    search_fields = ['start_time', 'end_time']
    
class searchCase(admin.ModelAdmin):
    search_fields = ['patient', 'submitter', 'lock_holder', 'specialties', 'submitter_comments']
    
class searchScan(admin.ModelAdmin):
    search_fields = ['patient', 'comments']
    
class searchAnnotation(admin.ModelAdmin):
    search_fields = ['picture', 'author', 'comments']

admin.site.register(Doctor, searchUser)
admin.site.register(Worker, searchUser)
admin.site.register(Patient, searchPatient)
admin.site.register(MeasurementType, searchMType)
admin.site.register(Measurement, searchMeasurement)
admin.site.register(SpecialtyType, searchSpeciality)
admin.site.register(TimeSlot, searchTimeslot)
admin.site.register(Case, searchCase)
admin.site.register(Scan, searchScan)
admin.site.register(Annotation, searchAnnotation)
