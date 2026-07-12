from django.urls import path
from .views import (
    RegisterMedecinView,
    ListeMedecinsView,
    DetailMedecinView,
)

urlpatterns = [
    path('',                  ListeMedecinsView.as_view()),   # GET
    path('inscription/',      RegisterMedecinView.as_view()), # POST
    path('<int:medecin_id>/', DetailMedecinView.as_view()),   # GET / PUT / DELETE
]