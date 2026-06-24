from django.core.exceptions import ValidationError
from django.db import models


class Notification(models.Model):
    utilisateur = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    rendez_vous = models.ForeignKey(
        "rendezvous.RendezVous",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )
    consultation = models.ForeignKey(
        "consultations.Consultation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-date_creation"]

    def clean(self):
        if not self.rendez_vous_id and not self.consultation_id:
            raise ValidationError(
                "Une notification doit être liée à un rendez-vous ou une consultation."
            )

    def __str__(self):
        statut = "lue" if self.lu else "non lue"
        return f"Notification pour {self.utilisateur} ({statut})"
