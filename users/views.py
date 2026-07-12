from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#ajout d'import
from rest_framework import generics, status
from .serializers import (
    RegisterResponsableSerializer,
    RegisterPatientSerializer,
    ChangePasswordSerializer,
    MyTokenSerializer,
)
from users.permissions import IsResponsable


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenSerializer


class MyTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class MyLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # ← Django donne l'user connecté automatiquement

        data = {
            "id":       user.id,
            "username": user.username,
            "email":    user.email,
            "role":     user.role,
        }

        # Selon le rôle → on ajoute le bon profil
        if user.role == 'medecin':
            try:
                profil = user.medecin  # ← related_name='medecin'
                data['profil'] = {
                    "profil_id":  profil.id,
                    "specialite": profil.specialite,
                    "telephone":  profil.telephone,
                }
            except:
                data['profil'] = None

        elif user.role == 'patient':
            try:
                profil = user.patient  # ← related_name='patient'
                data['profil'] = {
                    "profil_id":     profil.id,
                    "date_naissance": str(profil.date_naissance),
                    "adresse":        profil.adresse,
                    "telephone":      profil.telephone,
                }
            except:
                data['profil'] = None

        elif user.role == 'responsable':
            try:
                profil = user.responsable  # ← related_name='responsable'
                data['profil'] = {
                    "profil_id":   profil.id,
                    "departement": profil.departement,
                }
            except:
                data['profil'] = None

        return Response(data)
    

#ajout des classes pour l'inscription des patients et responsables, ainsi que le changement de mot de passe
class RegisterResponsableView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterResponsableSerializer


class RegisterPatientView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterPatientSerializer

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Mot de passe modifié avec succès."},
            status=status.HTTP_200_OK
        )