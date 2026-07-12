from django.db import models
from django.conf import settings


class Notification(models.Model):

    class Type(models.TextChoices):
        RDV_CONFIRME = 'rdv_confirme', 'RDV Confirmé'
        RDV_ANNULE   = 'rdv_annule',   'RDV Annulé'
        RDV_RAPPEL   = 'rdv_rappel',   'Rappel RDV'
        CONSULTATION = 'consultation', 'Nouvelle Consultation'
        SYSTEME      = 'systeme',      'Système'

    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type         = models.CharField(max_length=30, choices=Type.choices)
    titre        = models.CharField(max_length=200)
    message      = models.TextField()
    lu           = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Notification"
        verbose_name_plural = "Notifications"
        ordering            = ['-created_at']

    def __str__(self):
        return f"[{self.type}] {self.destinataire.username} — {self.titre}"