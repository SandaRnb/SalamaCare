from django.db import models
from django.conf import settings


class ProfilMedecin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    specialite = models.CharField(max_length=100)
    telephone  = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"
        

    def __str__(self):
        return f"Dr. {self.user.username}"
