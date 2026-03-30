from django.db import models
from django.contrib.auth.models import User

# 1. Patient Model
class Patient(models.Model):
    # Links to Django's built-in User model for authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# 2. Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Dr. {self.user.last_name} ({self.specialty})"

# 3. Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date}"

# 4. Medical Record Model
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    record_type = models.CharField(max_length=100) # e.g., Blood Test, X-Ray
    date_issued = models.DateField()
    result_summary = models.CharField(max_length=255)
    detailed_notes = models.TextField()

    def __str__(self):
        return f"{self.record_type} - {self.patient}"