from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("responsable", "Responsable"),
        ("medecin", "Médecin"),
        ("patient", "Patient"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    mail = models.EmailField()
    mot_de_passe = models.CharField(max_length=100)

class ProfilMedecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)
    numero_chambre = models.IntegerField()

class ProfilPatient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=200)
    sexe = models.CharField(max_length=100)

class ProfilResponsable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departement = models.CharField(max_length=100)