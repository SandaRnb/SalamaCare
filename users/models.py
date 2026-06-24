from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r"^\+?[\d\s\-]{8,20}$",
    message="Numéro de téléphone invalide.",
)


def validate_date_naissance(value):
    if value > timezone.now().date():
        raise ValidationError("La date de naissance ne peut pas être dans le futur.")


class User(AbstractUser):
    class Role(models.TextChoices):
        RESPONSABLE = "responsable", "Responsable"
        MEDECIN = "medecin", "Médecin"
        PATIENT = "patient", "Patient"

    role = models.CharField(max_length=20, choices=Role.choices)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(
        max_length=20,
        unique=True,
        validators=[phone_validator],
    )
    email = models.EmailField("Mail", unique=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(role__in=["responsable", "medecin", "patient"]),
                name="users_user_role_valide",
            ),
        ]

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.get_role_display()})"

class ProfilMedecin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profil_medecin",
    )
    specialite = models.CharField(max_length=100)
    numero_chambre = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(numero_chambre__gt=0),
                name="profil_medecin_chambre_positive",
            ),
        ]

    def clean(self):
        if self.user_id and self.user.role != User.Role.MEDECIN:
            raise ValidationError(
                {"user": "Seul un utilisateur avec le rôle médecin peut avoir ce profil."}
            )

    def __str__(self):
        return f"Dr {self.user.prenom} {self.user.nom} — {self.specialite}"


class ProfilPatient(models.Model):
    class Sexe(models.TextChoices):
        MASCULIN = "M", "Masculin"
        FEMININ = "F", "Féminin"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profil_patient",
    )
    date_naissance = models.DateField(validators=[validate_date_naissance])
    adresse = models.CharField(max_length=200)
    sexe = models.CharField(max_length=1, choices=Sexe.choices)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(sexe__in=["M", "F"]),
                name="profil_patient_sexe_valide",
            ),
        ]

    def clean(self):
        if self.user_id and self.user.role != User.Role.PATIENT:
            raise ValidationError(
                {"user": "Seul un utilisateur avec le rôle patient peut avoir ce profil."}
            )

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom}"


class ProfilResponsable(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profil_responsable",
    )
    departement = models.CharField(max_length=100)

    def clean(self):
        if self.user_id and self.user.role != User.Role.RESPONSABLE:
            raise ValidationError(
                {
                    "user": "Seul un utilisateur avec le rôle responsable peut avoir ce profil."
                }
            )

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom} — {self.departement}"
