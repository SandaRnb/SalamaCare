from django.db import models
from django.conf import settings


class ProfilPatient(models.Model):
    user           = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient'
    )
    date_naissance = models.DateField()
    adresse        = models.CharField(max_length=200)
    telephone      = models.CharField(max_length=20)

    class Meta:
        verbose_name        = "Patient"
        verbose_name_plural = "Patients"
        ordering            = ['user__last_name']

    def __str__(self):
        return f"Patient {self.user.username}"