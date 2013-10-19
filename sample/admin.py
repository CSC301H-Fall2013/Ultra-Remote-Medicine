from django.contrib import admin

from sample.models import (Doctor, Worker, Patient, Measurement,
        MeasurementType, SpecialtyType, TimeSlot, Case, Scan, Annotation)

admin.site.register(Doctor)
admin.site.register(Worker)
admin.site.register(Patient)
admin.site.register(MeasurementType)
admin.site.register(Measurement)
admin.site.register(SpecialtyType)
admin.site.register(TimeSlot)
admin.site.register(Case)
admin.site.register(Scan)
admin.site.register(Annotation)
