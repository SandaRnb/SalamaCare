from django.urls import path
from .views import (
    RegisterPatientView,
    ListePatientsView,
    DetailPatientView,
)

urlpatterns = [
    path('',                  ListePatientsView.as_view()),    # GET
    path('inscription/',      RegisterPatientView.as_view()),  # POST
    path('<int:patient_id>/', DetailPatientView.as_view()),    # GET / PUT / DELETE
]