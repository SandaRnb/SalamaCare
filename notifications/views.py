from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import NotificationSerializer
from .services import (
    get_notifications_user,
    get_notifications_non_lues,
    marquer_comme_lu,
    marquer_tout_lu,
    supprimer_notification,
)


class ListeNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = get_notifications_user(request.user)
        serializer    = NotificationSerializer(notifications, many=True)
        return Response({"notifications": serializer.data})


class NotificationsNonLuesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = get_notifications_non_lues(request.user)
        serializer    = NotificationSerializer(notifications, many=True)
        return Response({
            "non_lues":  serializer.data,
            "total":     notifications.count(),
        })


class MarquerLuView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, notification_id):
        notification = marquer_comme_lu(notification_id, request.user)
        if not notification:
            return Response(
                {"erreur": "Notification introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = NotificationSerializer(notification)
        return Response({"message": "Notification lue", "notification": serializer.data})


class MarquerToutLuView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        marquer_tout_lu(request.user)
        return Response({"message": "Toutes les notifications marquées comme lues"})


class SupprimerNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, notification_id):
        ok = supprimer_notification(notification_id, request.user)
        if not ok:
            return Response(
                {"erreur": "Notification introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({"message": "Notification supprimée"})