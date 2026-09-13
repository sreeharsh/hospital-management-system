from django.contrib import admin
from .models import Patient,Doctor,DoctorSchedule,Appointment

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(DoctorSchedule)
admin.site.register(Appointment)