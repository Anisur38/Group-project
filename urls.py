from django.urls import path
from . import views

urlpatterns = [
    # Renders the HTML frontend
    path('', views.index, name='index'), 
    
    # API endpoints for fetching and posting data
    path('api/dashboard/', views.get_patient_dashboard_data, name='api_dashboard'),
    path('api/records/', views.get_medical_records, name='api_records'),
    path('api/doctors/', views.get_doctors_list, name='api_doctors'),
    path('api/book/', views.book_appointment, name='api_book'),
]