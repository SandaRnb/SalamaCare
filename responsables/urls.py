from django.urls import path
from .views import PatientRechercheView, StatutPatientsView

urlpatterns = [
    path('patients/recherche/', PatientRechercheView.as_view(), name='responsable-patient-recherche'),
    path('patients/statut/', StatutPatientsView.as_view(), name='responsable-statut-patients'),
]