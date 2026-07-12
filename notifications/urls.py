from django.urls import path
from .views import (
    ListeNotificationsView,
    NotificationsNonLuesView,
    MarquerLuView,
    MarquerToutLuView,
    SupprimerNotificationView,
)

urlpatterns = [
    path('',                          ListeNotificationsView.as_view()),    # GET
    path('non-lues/',                 NotificationsNonLuesView.as_view()),  # GET
    path('tout-lu/',                  MarquerToutLuView.as_view()),         # PUT
    path('<int:notification_id>/lu/', MarquerLuView.as_view()),             # PUT
    path('<int:notification_id>/',    SupprimerNotificationView.as_view()), # DELETE
]