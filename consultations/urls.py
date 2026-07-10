# consultations/urls.py
from django.urls import path
from .views import (
    ConsultationListView,
    ConsultationDetailView,
    ConsultationPatientView,
    OrdonnanceListView,
    OrdonnanceDeleteView,
)

urlpatterns = [
    # consultations
    path("",
         ConsultationListView.as_view()),

    path("<int:pk>/",
         ConsultationDetailView.as_view()),

    path("patient/<int:patient_id>/",
         ConsultationPatientView.as_view()),

    # ordonnances
    path("<int:consultation_id>/ordonnances/",
         OrdonnanceListView.as_view()),

    path("ordonnances/<int:pk>/",
         OrdonnanceDeleteView.as_view()),
]