from .models import Notification


def get_notifications_user(user):
    """Toutes les notifications d'un user"""
    return Notification.objects.filter(destinataire=user)


def get_notifications_non_lues(user):
    """Notifications non lues d'un user"""
    return Notification.objects.filter(destinataire=user, lu=False)


def envoyer_notification(destinataire, type, titre, message):
    """Crée une notification pour un user"""
    return Notification.objects.create(
        destinataire = destinataire,
        type         = type,
        titre        = titre,
        message      = message,
    )


def marquer_comme_lu(notification_id, user):
    try:
        notification    = Notification.objects.get(id=notification_id, destinataire=user)
        notification.lu = True
        notification.save()
        return notification
    except Notification.DoesNotExist:
        return None


def marquer_tout_lu(user):
    """Marque toutes les notifications comme lues"""
    Notification.objects.filter(destinataire=user, lu=False).update(lu=True)


def supprimer_notification(notification_id, user):
    try:
        notification = Notification.objects.get(id=notification_id, destinataire=user)
        notification.delete()
        return True
    except Notification.DoesNotExist:
        return False