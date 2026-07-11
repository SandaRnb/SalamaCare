from django.db import models
from rendezvous.models import RendezVous
from medecins.models import ProfilMedecin
from patients.models import ProfilPatient


class Consultation(models.Model):
    rendez_vous = models.OneToOneField(
        RendezVous,
        on_delete=models.CASCADE,
        related_name='consultation'
    )
    patient     = models.ForeignKey(
        ProfilPatient,
        on_delete=models.CASCADE,
        related_name='consultations'
    )
    medecin     = models.ForeignKey(
        ProfilMedecin,
        on_delete=models.CASCADE,
        related_name='consultations'
    )
    diagnostic  = models.TextField()
    traitement  = models.TextField(blank=True)
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Consultation"
        verbose_name_plural = "Consultations"
        ordering            = ['-created_at']

    def __str__(self):
        return f"Consultation {self.patient} — Dr.{self.medecin} | {self.created_at}"


class Ordonnance(models.Model):
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='ordonnances'
    )
    medicament   = models.CharField(max_length=200)
    posologie    = models.TextField()
    duree        = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medicament} — {self.posologie}"
        