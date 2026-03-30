from django.contrib import admin
from .models import Patient, Doctor, Appointment, MedicalRecord


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'contact_number', 'blood_group')
    search_fields = ('user__first_name', 'user__last_name', 'contact_number')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'department')
    search_fields = ('user__last_name', 'specialty')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'doctor')
    
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_type', 'date_issued', 'doctor')
    list_filter = ('date_issued', 'record_type')