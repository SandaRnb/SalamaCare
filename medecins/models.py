from django.core.exceptions import ValidationError
from django.db import models


class Disponibilite(models.Model):
    class JourSemaine(models.IntegerChoices):
        LUNDI = 1, "Lundi"
        MARDI = 2, "Mardi"
        MERCREDI = 3, "Mercredi"
        JEUDI = 4, "Jeudi"
        VENDREDI = 5, "Vendredi"
        SAMEDI = 6, "Samedi"
        DIMANCHE = 7, "Dimanche"

    profil_medecin = models.ForeignKey(
        "users.ProfilMedecin",
        on_delete=models.CASCADE,
        related_name="disponibilites",
    )
    jour = models.IntegerField(choices=JourSemaine.choices)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        verbose_name = "Disponibilité"
        verbose_name_plural = "Disponibilités"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(heure_fin__gt=models.F("heure_debut")),
                name="disponibilite_heure_fin_apres_debut",
            ),
            models.UniqueConstraint(
                fields=["profil_medecin", "jour", "heure_debut"],
                name="disponibilite_creneau_unique",
            ),
        ]
        ordering = ["jour", "heure_debut"]

    def clean(self):
        if self.heure_debut and self.heure_fin and self.heure_fin <= self.heure_debut:
            raise ValidationError(
                {"heure_fin": "L'heure de fin doit être postérieure à l'heure de début."}
            )

    def __str__(self):
        return (
            f"{self.profil_medecin} — "
            f"{self.get_jour_display()} {self.heure_debut:%H:%M}-{self.heure_fin:%H:%M}"
        )
