from rest_framework import serializers
from patients.models import ProfilPatient


class PatientRechercheSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email    = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = ProfilPatient
        fields = ['id', 'username', 'email', 'date_naissance', 'adresse', 'telephone']
