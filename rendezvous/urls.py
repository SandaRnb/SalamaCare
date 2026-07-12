from django.urls import path
from .views import (
    ListeRendezVousView,
    CreerRendezVousView,
    DetailRendezVousView,
    ModifierStatutView,
    RendezVousPatientView,
    RendezVousMedecinView,
)

urlpatterns = [
    path('',                              ListeRendezVousView.as_view()),    # GET
    path('creer/',                        CreerRendezVousView.as_view()),    # POST
    path('<int:rdv_id>/',                 DetailRendezVousView.as_view()),   # GET / DELETE
    path('<int:rdv_id>/statut/',          ModifierStatutView.as_view()),     # PUT
    path('patient/<int:patient_id>/',     RendezVousPatientView.as_view()),  # GET
    path('medecin/<int:medecin_id>/',     RendezVousMedecinView.as_view()),  # GET
]