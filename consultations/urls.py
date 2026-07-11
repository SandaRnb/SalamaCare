from django.urls import path
from .views import (
    ListeConsultationsView,
    CreerConsultationView,
    DetailConsultationView,
    ConsultationsPatientView,
    ConsultationsMedecinView,
    OrdonnanceView,
)

urlpatterns = [
    path('',                                          ListeConsultationsView.as_view()),   # GET
    path('creer/',                                    CreerConsultationView.as_view()),    # POST
    path('<int:consultation_id>/',                    DetailConsultationView.as_view()),   # GET/PUT/DELETE
    path('patient/<int:patient_id>/',                 ConsultationsPatientView.as_view()), # GET
    path('medecin/<int:medecin_id>/',                 ConsultationsMedecinView.as_view()), # GET
    path('<int:consultation_id>/ordonnances/',         OrdonnanceView.as_view()),           # POST
    path('<int:consultation_id>/ordonnances/<int:ordonnance_id>/', OrdonnanceView.as_view()), # DELETE
]