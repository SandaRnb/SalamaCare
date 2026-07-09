from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Authentification ──────────────────────────────
    path("api/token/",                 TokenObtainPairView.as_view()),
    path("api/token/refresh/",         TokenRefreshView.as_view()),

    # ── Apps ──────────────────────────────
    path('api/users/',         include('users.urls')),
    path('api/medecins/',      include('medecins.urls')),
    path('api/patients/',      include('patients.urls')),
    path('api/rendezvous/',    include('rendezvous.urls')),
    # path('api/consultations/', include('consultations.urls')),
    # path('api/notifications/', include('notifications.urls')),
]
