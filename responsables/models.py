from django.db import models
from django.conf import settings


class ProfilResponsable(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    departement = models.CharField(max_length=100)

    def __str__(self):
        return f"Responsable {self.user.username}"
