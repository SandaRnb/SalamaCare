from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ProfilPatient

User = get_user_model()


# Inscription
class RegisterPatientSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )
    date_naissance = serializers.DateField()
    adresse        = serializers.CharField()
    telephone      = serializers.CharField()

    class Meta:
        model  = User
        fields = [
            "username", "email",
            "password", "password2",
            "date_naissance", "adresse", "telephone"
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        date_naissance = validated_data.pop("date_naissance")
        adresse        = validated_data.pop("adresse")
        telephone      = validated_data.pop("telephone")

        user = User.objects.create_user(
            **validated_data,
            role=User.Role.PATIENT
        )
        ProfilPatient.objects.create(
            user           = user,
            date_naissance = date_naissance,
            adresse        = adresse,
            telephone      = telephone,
        )
        return user


# Affichage
class ProfilPatientSerializer(serializers.ModelSerializer):
    nom      = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email    = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model  = ProfilPatient
        fields = ['id', 'nom', 'username', 'email', 'date_naissance', 'adresse', 'telephone']