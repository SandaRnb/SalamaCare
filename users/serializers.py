from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from patients.models import ProfilPatient
from medecins.models import ProfilMedecin
from responsable.models import ProfilResponsable



# ─── Token avec rôle
class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"]  = user.role
        token["email"] = user.email
        return token


# ─── Inscription Médecin
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


# ─── Inscription Patient
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
            user=user,
            date_naissance=date_naissance,
            adresse=adresse,
            telephone=telephone
        )
        return user


# ─── Inscription Responsable
class RegisterResponsableSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )
    departement = serializers.CharField()

    class Meta:
        model  = User
        fields = [
            "username", "email",
            "password", "password2",
            "departement"
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        departement = validated_data.pop("departement")

        user = User.objects.create_user(
            **validated_data,
            role=User.Role.RESPONSABLE
        )
        ProfilResponsable.objects.create(
            user=user,
            departement=departement
        )
        return user


# ─── Changement de mot de passe
class ChangePasswordSerializer(serializers.Serializer):
    ancien_password   = serializers.CharField(write_only=True)
    nouveau_password  = serializers.CharField(
        write_only=True,
        min_length=8
    )
    nouveau_password2 = serializers.CharField(write_only=True)

    def validate_ancien_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Ancien mot de passe incorrect."
            )
        return value

    def validate(self, data):
        if data["nouveau_password"] != data["nouveau_password2"]:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return data

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["nouveau_password"])
        user.save()