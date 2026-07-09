from rest_framework import serializers
from .models import RendezVous
from medecins.models import ProfilMedecin
from patients.models import ProfilPatient


# ── Affichage ─────────────────────────────────────────────
class RendezVousSerializer(serializers.ModelSerializer):

    # Infos du patient
    patient_nom      = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    patient_username = serializers.CharField(source='patient.user.username',      read_only=True)

    # Infos du médecin
    medecin_nom      = serializers.CharField(source='medecin.user.get_full_name', read_only=True)
    medecin_spec     = serializers.CharField(source='medecin.specialite',         read_only=True)

    class Meta:
        model  = RendezVous
        fields = [
            'id',
            'patient_nom', 'patient_username',
            'medecin_nom', 'medecin_spec',
            'date_heure', 'motif', 'statut',
            'created_at',
        ]


# ── Création ──────────────────────────────────────────────
class CreerRendezVousSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    medecin_id = serializers.IntegerField()
    date_heure = serializers.DateTimeField()
    motif      = serializers.CharField()

    def validate_patient_id(self, value):
        if not ProfilPatient.objects.filter(id=value).exists():
            raise serializers.ValidationError("Patient introuvable")
        return value

    def validate_medecin_id(self, value):
        if not ProfilMedecin.objects.filter(id=value).exists():
            raise serializers.ValidationError("Médecin introuvable")
        return value


# ── Modification statut ───────────────────────────────────
class ModifierStatutSerializer(serializers.Serializer):
    statut = serializers.ChoiceField(choices=RendezVous.Statut.choices)