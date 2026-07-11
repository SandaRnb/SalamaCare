from django.urls import path
from .views import PatientRechercheView

urlpatterns = [
    path('patients/recherche/', PatientRechercheView.as_view(), name='responsable-patient-recherche'),
]