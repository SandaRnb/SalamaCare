from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        RESPONSABLE = "responsable", "Responsable"
        MEDECIN     = "medecin",     "Médecin"
        PATIENT     = "patient",     "Patient"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class ProfilMedecin(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)
    telephone  = models.CharField(max_length=20)

    def __str__(self):
        return f"Dr. {self.user.username}"


class ProfilPatient(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    date_naissance = models.DateField()
    adresse        = models.CharField(max_length=200)
    telephone      = models.CharField(max_length=20)

    def __str__(self):
        return f"Patient {self.user.username}"


class ProfilResponsable(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    departement = models.CharField(max_length=100)

    def __str__(self):
        return f"Responsable {self.user.username}"