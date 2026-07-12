from rest_framework import serializers
from patients.models import ProfilPatient
from rendezvous.models import RendezVous


class PatientRechercheSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email    = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = ProfilPatient
        fields = ['id', 'username', 'email', 'date_naissance', 'adresse', 'telephone']





class StatutPatientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    statut   = serializers.SerializerMethodField()

    class Meta:
        model = ProfilPatient
        fields = ['id', 'username', 'statut']

    def get_statut(self, obj):
        dernier_rdv = RendezVous.objects.filter(patient=obj).order_by('-date_heure').first()
        if dernier_rdv:
            return dernier_rdv.statut
        return 'aucun_rdv'