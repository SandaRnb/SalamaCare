from rest_framework import serializers
from .models import Consultation, Ordonnance


# ─── Ordonnance ───────────────────────────────────────────────
class OrdonnanceSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Ordonnance
        fields = [
            "id",
            "medicament",
            "posologie",
            "duree"
        ]


# ─── Consultation ─────────────────────────────────────────────
class ConsultationSerializer(serializers.ModelSerializer):
    ordonnances = OrdonnanceSerializer(many=True, read_only=True)

    class Meta:
        model  = Consultation
        fields = [
            "id",
            "rendez_vous",
            "patient",
            "medecin",
            "diagnostic",
            "traitement",
            "notes",
            "ordonnances",
            "created_at"
        ]
        read_only_fields = ["created_at"]


# ─── Création consultation ────────────────────────────────────
class ConsultationCreateSerializer(serializers.ModelSerializer):
    ordonnances = OrdonnanceSerializer(many=True, required=False)

    class Meta:
        model  = Consultation
        fields = [
            "rendez_vous",
            "patient",
            "medecin",
            "diagnostic",
            "traitement",
            "notes",
            "ordonnances"
        ]

    def validate_rendez_vous(self, value):
        # vérifier qu'une consultation n'existe pas déjà pour ce rdv
        if Consultation.objects.filter(rendez_vous=value).exists():
            raise serializers.ValidationError(
                "Une consultation existe déjà pour ce rendez-vous."
            )
        return value

    def create(self, validated_data):
        ordonnances_data = validated_data.pop("ordonnances", [])

        # créer la consultation
        consultation = Consultation.objects.create(**validated_data)

        # créer les ordonnances liées
        for ordonnance_data in ordonnances_data:
            Ordonnance.objects.create(
                consultation=consultation,
                **ordonnance_data
            )
        return consultation


# ─── Mise à jour consultation ─────────────────────────────────
class ConsultationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Consultation
        fields = [
            "diagnostic",
            "traitement",
            "notes"
        ]