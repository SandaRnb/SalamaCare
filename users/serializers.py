from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email    = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email ou mot de passe incorrect")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Email ou mot de passe incorrect")

        data['user'] = user
        return data