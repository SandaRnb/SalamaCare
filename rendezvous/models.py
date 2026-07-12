from django.db import models
from medecins.models import ProfilMedecin
from patients.models import ProfilPatient

class RendezVous(models.Model):

    class Statut(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'En attente'
        CONFIRME   = 'confirme',   'Confirmé'
        ANNULE     = 'annule',     'Annulé'
        TERMINE    = 'termine',    'Terminé'

    patient    = models.ForeignKey(
        ProfilPatient,
        on_delete=models.CASCADE,
        related_name='rendez_vous'
    )
    medecin    = models.ForeignKey(
        ProfilMedecin,
        on_delete=models.CASCADE,
        related_name='rendez_vous'
    )
    date_heure = models.DateTimeField()
    motif      = models.TextField()
    statut     = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering            = ['-date_heure']

    def __str__(self):
        return f"{self.patient.username} → Dr.{self.medecin.user.username} | {self.date_heure}"
