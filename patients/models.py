from django.db import models


class DossierPatient(models.Model):
    class GroupeSanguin(models.TextChoices):
        A_POS = "A+", "A+"
        A_NEG = "A-", "A-"
        B_POS = "B+", "B+"
        B_NEG = "B-", "B-"
        AB_POS = "AB+", "AB+"
        AB_NEG = "AB-", "AB-"
        O_POS = "O+", "O+"
        O_NEG = "O-", "O-"

    profil_patient = models.OneToOneField(
        "users.ProfilPatient",
        on_delete=models.CASCADE,
        related_name="dossier",
    )
    groupe_sanguin = models.CharField(
        max_length=3,
        choices=GroupeSanguin.choices,
    )
    antecedents = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dossier patient"
        verbose_name_plural = "Dossiers patients"

    def __str__(self):
        return f"Dossier de {self.profil_patient}"
