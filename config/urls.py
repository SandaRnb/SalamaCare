from django.contrib import admin
from django.urls import path, include
from users.views import MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Authentification ──────────────────────────────
    path("api/token/", MyTokenObtainPairView.as_view()),
    path("api/token/refresh/", MyTokenRefreshView.as_view()),

    # ── Apps ──────────────────────────────
    path('api/users/',         include('users.urls')),
    path('api/medecins/',      include('medecins.urls')),
    path('api/patients/',      include('patients.urls')),
    path('api/rendezvous/',    include('rendezvous.urls')),
    path('api/consultations/', include('consultations.urls')),
    # path('api/notifications/', include('notifications.urls')),
    path('api/responsables/', include('responsables.urls')),
]
