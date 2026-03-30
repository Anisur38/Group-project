from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Patient, Doctor, Appointment, MedicalRecord
import json

def index(request):
    """Renders the main HTML frontend."""
    return render(request, 'index.html')

def get_patient_dashboard_data(request):
    """API endpoint to fetch data for the patient dashboard."""
    # Note: For prototype testing without login setup, we just fetch the first patient.
    # In the final version with authentication, use: patient = request.user.patient
    patient = Patient.objects.first()
    if not patient:
        return JsonResponse({"error": "No patients found in database."}, status=404)

    upcoming_appts = Appointment.objects.filter(
        patient=patient, 
        status='SCHEDULED'
    ).order_by('appointment_date', 'appointment_time')
    
    data = {
        "patient_name": f"{patient.user.first_name} {patient.user.last_name}",
        "appointments": [
            {
                "id": appt.id,
                "doctor": str(appt.doctor),
                "date": appt.appointment_date.strftime("%b %d, %Y"),
                "time": appt.appointment_time.strftime("%I:%M %p"),
                "specialty": appt.doctor.specialty
            } for appt in upcoming_appts
        ]
    }
    return JsonResponse(data)

def get_medical_records(request):
    """API endpoint to fetch medical records for the patient."""
    patient = Patient.objects.first()
    if not patient:
         return JsonResponse({"error": "No patients found in database."}, status=404)

    records = MedicalRecord.objects.filter(patient=patient).order_by('-date_issued')
    
    data = [
        {
            "id": rec.id,
            "date": rec.date_issued.strftime("%b %d, %Y"),
            "type": rec.record_type,
            "doctor": str(rec.doctor),
            "result": rec.result_summary
        } for rec in records
    ]
    return JsonResponse({"records": data})

def get_doctors_list(request):
    """API endpoint to get list of doctors for the booking calendar."""
    doctors = Doctor.objects.all()
    data = [
        {"id": doc.id, "name": str(doc), "specialty": doc.specialty} 
        for doc in doctors
    ]
    return JsonResponse({"doctors": data})

@csrf_exempt
def book_appointment(request):
    """API endpoint to handle booking a new appointment via POST request."""
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            patient = Patient.objects.first() 
            doctor = get_object_or_404(Doctor, id=body['doctor_id'])
            
            new_appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=body['date'],
                appointment_time=body['time'],
                reason=body.get('reason', '')
            )
            return JsonResponse({"status": "success", "appointment_id": new_appointment.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)