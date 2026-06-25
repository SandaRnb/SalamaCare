from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    MyLoginView,
    RegisterMedecinView,
    RegisterPatientView,
    RegisterResponsableView,
    ChangePasswordView,
)

urlpatterns = [
    # auth
    path("login/",                 MyLoginView.as_view()),
    path("token/refresh/",         TokenRefreshView.as_view()),

    # inscription
    path("register/medecin/",      RegisterMedecinView.as_view()),
    path("register/patient/",      RegisterPatientView.as_view()),
    path("register/responsable/",  RegisterResponsableView.as_view()),

    # mot de passe
    path("change-password/",       ChangePasswordView.as_view()),
]