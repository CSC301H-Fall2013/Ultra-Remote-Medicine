from django.db import models
from django.contrib.auth.models import User

'''
TODO:
- Review patient address representation.
- Review image linkage format.
- Decide whether or not some foreign/m2m keys should be put in both related
    tables (if even possible)
SUGGESTION:
- Maybe split User into Doctor and Administration
'''


class Doctor(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=63)
    address = models.CharField(max_length=254)
    registration_time = models.DateTimeField()
    specialties = models.ManyToManyField('SpecialtyType', blank=True,
                                         null=True)
    schedule = models.ManyToManyField('Schedule', blank=True)
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)


class Worker(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=63)
    address = models.CharField(max_length=254)
    registration_time = models.DateTimeField()
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)


class Patient(models.Model):
    user = models.OneToOneField(User)
    gps_coordinates = models.CharField(max_length=63, blank=True)
    address = models.CharField(max_length=254, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=63, blank=True)

    def __unicode__(self):
        return str(self.id)


class Measurement(models.Model):
    worker = models.ForeignKey(Worker)
    patient = models.ForeignKey(Patient)
    time_taken = models.DateTimeField()
    weight = models.IntegerField()
    height = models.IntegerField()

    def __unicode__(self):
        return "Measurement " + str(self.id)


class SpecialtyType(models.Model):
    name = models.CharField(max_length=63)

    def __unicode__(self):
        return str(self.id) + ". " + self.name


class Schedule(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__(self):
        return "Schedule " + str(self.id)


class Case(models.Model):
    patient = models.ForeignKey(Patient)
    submitter = models.ForeignKey(Worker, related_name='workercase')
    lock_holder = models.ForeignKey(Doctor, related_name='doctorcase',
                                    blank=True, null=True)

    specialties = models.ManyToManyField(SpecialtyType, blank=True, null=True)
    submitter_comments = models.TextField(blank=True)

    def __unicode__(self):
        return "Case " + str(self.id)


class CasePicture(models.Model):
    case = models.ForeignKey(Case)
    picture_linkage = models.URLField()
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return "Case Picture " + str(self.id)


class Annotation(models.Model):
    picture = models.ForeignKey(CasePicture)
    doctor = models.ForeignKey(Doctor)
    annotation_picture_linkage = models.URLField()
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return "Annotation " + str(self.id)
