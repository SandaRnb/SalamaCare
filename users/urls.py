from django.urls import path
from .views import MyLoginView

urlpatterns = [
    path("me/", MyLoginView.as_view())
]