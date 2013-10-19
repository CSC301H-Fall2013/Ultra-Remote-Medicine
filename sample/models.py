from django.db import models
from django.contrib.auth.models import User

'''
TODO:
- Review patient address representation.
- Review image linkage format.
- Decide whether or not some foreign/m2m keys should be put in both related
    tables (if even possible)
'''

''' Represents a doctor, the job of whom primarily is to annotate and review
    cases and scans submitted by workers, and issue instructions to patients
    and workers. '''
class Doctor(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=63)
    address = models.CharField(max_length=254)
    registration_time = models.DateTimeField()
    specialties = models.ManyToManyField('SpecialtyType', blank=True,
                                         null=True)
    schedule = models.ManyToManyField('TimeSlot', blank=True, null=True)
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)

''' Represents a worker, the job of whom primarily is to register new patients,
    submit new cases, and to take measurements, scans, pictures and other
    documentation.'''
class Worker(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=63)
    address = models.CharField(max_length=254)
    registration_time = models.DateTimeField()
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)

''' Represents a patient. Patients are not considered users, having no access
    to the server.'''
class Patient(models.Model):

    # In the future, patients may be considered users.
    # user = models.OneToOneField(User)

    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    gps_coordinates = models.CharField(max_length=63, blank=True)
    address = models.CharField(max_length=254, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=63, blank=True)
    health_id = models.CharField(max_length=63, blank=True, null=True)
    photo_link = models.URLField(blank=True)

    def __unicode__(self):
        return str(self.id) + ". " + self.last_name + ", " + self.first_name

''' MeasurementType entries record the different types of measurements that
    can be taken. All Measurement instances are of a particular
    MeasurementType.'''
class MeasurementType(models.Model):
    name = models.CharField(max_length=63)
    units = models.CharField(max_length=63)

    def __unicode__(self):
        return str(self.id) + ". " + self.name

''' A Measurement taken at a particular time of a patient. Each Measurement
    is of a particular MeasurementType.'''
class Measurement(models.Model):
    worker = models.ForeignKey(Worker)
    patient = models.ForeignKey(Patient)
    time_taken = models.DateTimeField()
    measurement_type = models.ForeignKey(MeasurementType)
    value = models.DecimalField(decimal_places=3, max_digits=15)

    def __unicode__(self):
        return "Measurement " + str(self.id)

''' SpecaialtyType entries record the different types of specialties that
    doctors can have. This is used instead of constant values or direct
    string values to encourage consistency.'''
class SpecialtyType(models.Model):
    name = models.CharField(max_length=63)

    def __unicode__(self):
        return str(self.id) + ". " + self.name

''' TimeSlot elements represent blocks of time that are available. Together,
    TimeSlot elements form a user's schedule. All times are stored in GMT.

    Note that this system is still under revision. '''
class TimeSlot(models.Model):

    # TODO: Restrict these so that they are weekly cycles, rather than a
    # single point in time.
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    ''' Converts the specified date_time to the format used by TimeSlot's
        __unicode__(...) implementation.'''
    def _convert_date_time_to_string(self, date_time):
        date_strings = ["Monday", "Tuesday", "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
        
        minute_string = str(date_time.minute)
        if len(minute_string) == 1:
            minute_string += "0"
            
        time_string = str(date_time.hour) + ":" + minute_string + " (GMT)"
        
        return date_strings[date_time.weekday()] + " " + time_string

    def __unicode__(self):
        return  (self._convert_date_time_to_string(self.start_time)
                 + " -> "
                 + self._convert_date_time_to_string(self.end_time))

''' Represents an original picture or scan of a Patient in the database.'''
class Scan(models.Model): 
    patient = models.ForeignKey(Patient)
    picture_linkage = models.URLField()
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return "Scan " + str(self.id)

''' Case entries represent individual problems that a Patient can have. A
    Case is "opened" when a user detects the problem and is "closed" when the
    problem is considered solved. '''
class Case(models.Model):

    # TODO: enforce a constraint where Case.scans.patient = Case.patient
    
    patient = models.ForeignKey(Patient)
    submitter = models.ForeignKey(Worker, db_column="Worker",
            related_name='workercase')
    lock_holder = models.ForeignKey(Doctor, db_column="Current Doctor",
            related_name='doctorcase', blank=True, null=True)
    specialties = models.ManyToManyField(SpecialtyType, blank=True, null=True)

    # This is more like one-to-many, but Django doesn't seem to support this,
    # except perhaps by having each Scan reference its associated Case (if
    # there is one).
    scans = models.ManyToManyField(Scan, blank=True, null=True)
    
    submitter_comments = models.TextField(blank=True)
    date_opened = models.DateField()
    date_closed = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return "Case " + str(self.id)

''' Represents an annotation made to a picture or scan of a Patient. Both
    workers and doctors can create annotations. '''
class Annotation(models.Model):
    picture = models.ForeignKey(Scan)
    author = models.ForeignKey(User)
    annotation_picture_linkage = models.URLField()
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return "Annotation " + str(self.id)
