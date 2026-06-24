from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class RendezVous(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        CONFIRME = "confirme", "Confirmé"
        ANNULE = "annule", "Annulé"

    profil_patient = models.ForeignKey(
        "users.ProfilPatient",
        on_delete=models.CASCADE,
        related_name="rendez_vous",
    )
    profil_medecin = models.ForeignKey(
        "users.ProfilMedecin",
        on_delete=models.CASCADE,
        related_name="rendez_vous",
    )
    date = models.DateField()
    heure = models.TimeField()
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE,
    )
    motif = models.CharField(max_length=255, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(statut__in=["en_attente", "confirme", "annule"]),
                name="rendezvous_statut_valide",
            ),
            models.UniqueConstraint(
                fields=["profil_medecin", "date", "heure"],
                condition=models.Q(statut__in=["en_attente", "confirme"]),
                name="rendezvous_creneau_medecin_unique",
            ),
        ]
        ordering = ["date", "heure"]

    def clean(self):
        if self.date and self.heure:
            rdv_datetime = timezone.make_aware(datetime.combine(self.date, self.heure))
            if rdv_datetime < timezone.now():
                raise ValidationError(
                    "La date et l'heure du rendez-vous ne peuvent pas être dans le passé."
                )

    def __str__(self):
        return (
            f"RDV {self.date} {self.heure:%H:%M} — "
            f"{self.profil_patient} / {self.profil_medecin}"
        )
