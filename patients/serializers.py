from django.utils.text import slugify
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ProfilPatient

User = get_user_model()


def build_username_from_email(email: str) -> str:
    base = slugify((email or '').split('@')[0] or 'user') or 'user'
    username = base
    counter = 1

    while User.objects.filter(username__iexact=username).exists():
        username = f"{base}{counter}"
        counter += 1

    return username


# Inscription
class RegisterPatientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
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

        if not data.get("username"):
            data["username"] = build_username_from_email(data.get("email", ""))

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