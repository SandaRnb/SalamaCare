from django.utils.text import slugify
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from medecins.models import ProfilMedecin
from patients.models import ProfilPatient
from responsables.models import ProfilResponsable


def build_username_from_email(email: str) -> str:
    base = slugify((email or '').split('@')[0] or 'user') or 'user'
    username = base
    counter = 1

    while User.objects.filter(username__iexact=username).exists():
        username = f"{base}{counter}"
        counter += 1

    return username


# ─── Token avec rôle
class MyTokenSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=False, allow_blank=True, write_only=True)
    email = serializers.EmailField(required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = False
        self.fields["username"].allow_blank = True

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")

        if email:
            account = User.objects.filter(email__iexact=email).first()
            if not account:
                raise serializers.ValidationError(
                    {"email": "Aucun compte trouvé pour cet email."}
                )
            attrs["username"] = account.username

        if not username and not email:
            raise serializers.ValidationError(
                {"username": "Le champ username ou email est requis."}
            )

        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        return token
    
# ─── Inscription Patient
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
    date_naissance = serializers.DateField(write_only=True)
    adresse        = serializers.CharField(write_only=True)
    telephone      = serializers.CharField(write_only=True)

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
            user=user,
            date_naissance=date_naissance,
            adresse=adresse,
            telephone=telephone
        )
        return user


# ─── Inscription Responsable
class RegisterResponsableSerializer(serializers.ModelSerializer):
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
    departement = serializers.CharField(write_only=True)

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

        if not data.get("username"):
            data["username"] = build_username_from_email(data.get("email", ""))

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