from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.liste_medecins),
    path('<int:medecin_id>/',   views.detail_medecin),
    path('creer/',              views.creer_medecin_view),
    path('<int:medecin_id>/modifier/',   views.modifier_medecin_view),
    path('<int:medecin_id>/supprimer/',  views.supprimer_medecin_view),
]