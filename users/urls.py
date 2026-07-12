from django.urls import path
<<<<<<< HEAD
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
=======
from .views import LoginView, MonProfilView

urlpatterns = [
    path('login/', LoginView.as_view()),  # POST
    path('moi/',   MonProfilView.as_view()),  # GET
>>>>>>> origin/natha-feature
]