from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    destinataire_username = serializers.CharField(
        source='destinataire.username',
        read_only=True
    )

    class Meta:
        model  = Notification
        fields = [
            'id',
            'destinataire_username',
            'type', 'titre', 'message',
            'lu', 'created_at',
        ]