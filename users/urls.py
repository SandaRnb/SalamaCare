from django.urls import path
from .views import LoginView, MonProfilView

urlpatterns = [
    path('login/', LoginView.as_view()),  # POST
    path('moi/',   MonProfilView.as_view()),  # GET
]