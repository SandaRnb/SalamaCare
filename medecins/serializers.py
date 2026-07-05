from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ProfilMedecin

User = get_user_model()


# ✅ Serializer inscription — version collab (on garde tel quel)
class RegisterMedecinSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )
    specialite = serializers.CharField()
    telephone  = serializers.CharField()

    class Meta:
        model  = User
        fields = [
            "username", "email",
            "password", "password2",
            "specialite", "telephone"
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        specialite = validated_data.pop("specialite")
        telephone  = validated_data.pop("telephone")

        user = User.objects.create_user(
            **validated_data,
            role=User.Role.MEDECIN
        )
        ProfilMedecin.objects.create(
            user=user,
            specialite=specialite,
            telephone=telephone
        )
        return user


# ✅ Serializer affichage — pour liste et détail
class ProfilMedecinSerializer(serializers.ModelSerializer):
    nom      = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email    = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model  = ProfilMedecin
        fields = ['id', 'nom', 'username', 'email', 'specialite', 'telephone']