from django.conf import settings
from django.db import models

class ProfilMedecin(models.Model):
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)
    telephone  = models.CharField(max_length=20)

    def __str__(self):
        return f"Dr. {self.user.username}"