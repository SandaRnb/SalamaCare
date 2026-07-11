from rest_framework import serializers
from .models import Consultation, Ordonnance


class OrdonnanceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Ordonnance
        fields = ['id', 'medicament', 'posologie', 'duree']


class ConsultationSerializer(serializers.ModelSerializer):
    patient_nom = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    medecin_nom = serializers.CharField(source='medecin.user.get_full_name', read_only=True)
    ordonnances = OrdonnanceSerializer(many=True, read_only=True)

    class Meta:
        model  = Consultation
        fields = [
            'id',
            'patient_nom', 'medecin_nom',
            'diagnostic', 'traitement', 'notes',
            'ordonnances',
            'created_at',
        ]


class CreerConsultationSerializer(serializers.Serializer):
    rdv_id     = serializers.IntegerField()
    diagnostic = serializers.CharField()
    traitement = serializers.CharField(required=False, default='')
    notes      = serializers.CharField(required=False, default='')


class AjouterOrdonnanceSerializer(serializers.Serializer):
    medicament = serializers.CharField()
    posologie  = serializers.CharField()
    duree      = serializers.CharField()