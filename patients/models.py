from django.conf import settings
from django.db import models

class ProfilPatient(models.Model):
    user           = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_naissance = models.DateField()
    adresse        = models.CharField(max_length=200)
    telephone      = models.CharField(max_length=20)

    def __str__(self):
        return f"Patient {self.user.username}"