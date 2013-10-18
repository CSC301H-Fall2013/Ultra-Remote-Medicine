from django.contrib import admin

from sample.models import Doctor, Worker, Patient, Measurement, SpecialtyType,\
    Schedule, Case, CasePicture, Annotation

admin.site.register(Doctor)
admin.site.register(Worker)
admin.site.register(Patient)
admin.site.register(Measurement)
admin.site.register(SpecialtyType)
admin.site.register(Schedule)
admin.site.register(Case)
admin.site.register(CasePicture)
admin.site.register(Annotation)
