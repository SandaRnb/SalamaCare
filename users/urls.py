from django.urls import path
from .views import (
    MyLoginView,
    RegisterResponsableView,
    RegisterPatientView,
    ChangePasswordView,
)

urlpatterns = [
    path("me/", MyLoginView.as_view()),
    path("register/responsable/", RegisterResponsableView.as_view()),
    path("register/patient/", RegisterPatientView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
]