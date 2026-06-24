from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, ProfilMedecin, ProfilPatient, ProfilResponsable

class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"]  = user.role
        token["email"] = user.email
        return token

class RegisterMedecinSerializer(serializers.ModelSerializer):
    password   = serializers.CharField(write_only=True)
    specialite = serializers.CharField()
    telephone  = serializers.CharField()

    class Meta:
        model  = User
        fields = ["username", "email", "password", "specialite", "telephone"]

    def create(self, validated_data):
        specialite = validated_data.pop("specialite")
        telephone  = validated_data.pop("telephone")
        user = User.objects.create_user(**validated_data, role="medecin")
        ProfilMedecin.objects.create(user=user, specialite=specialite, telephone=telephone)
        return user

class RegisterPatientSerializer(serializers.ModelSerializer):
    password       = serializers.CharField(write_only=True)
    date_naissance = serializers.DateField()
    adresse        = serializers.CharField()
    telephone      = serializers.CharField()

    class Meta:
        model  = User
        fields = ["username", "email", "password", "date_naissance", "adresse", "telephone"]

    def create(self, validated_data):
        date_naissance = validated_data.pop("date_naissance")
        adresse        = validated_data.pop("adresse")
        telephone      = validated_data.pop("telephone")
        user = User.objects.create_user(**validated_data, role="patient")
        ProfilPatient.objects.create(user=user, date_naissance=date_naissance,
                                     adresse=adresse, telephone=telephone)
        return user

class RegisterResponsableSerializer(serializers.ModelSerializer):
    password    = serializers.CharField(write_only=True)
    departement = serializers.CharField()

    class Meta:
        model  = User
        fields = ["username", "email", "password", "departement"]

    def create(self, validated_data):
        departement = validated_data.pop("departement")
        user = User.objects.create_user(**validated_data, role="responsable")
        ProfilResponsable.objects.create(user=user, departement=departement)
        return user