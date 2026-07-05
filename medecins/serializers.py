from rest_framework import serializers
from users.models import User
from .models import ProfilMedecin


class ProfilMedecinSerializer(serializers.ModelSerializer):

    # Champs venant de User
    nom      = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username')
    email    = serializers.EmailField(source='user.email')

    class Meta:
        model  = ProfilMedecin
        fields = ['id', 'nom', 'username', 'email', 'specialite', 'telephone']