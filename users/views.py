from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status

from .serializers import (
    RegisterResponsableSerializer,
    RegisterPatientSerializer,
    ChangePasswordSerializer,
)
from users.permissions import IsResponsable


class MyLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        data = {
            "id":       user.id,
            "username": user.username,
            "email":    user.email,
            "role":     user.role,
        }

        if user.role == 'medecin':
            try:
                profil = user.medecin
                data['profil'] = {
                    "profil_id":  profil.id,
                    "specialite": profil.specialite,
                    "telephone":  profil.telephone,
                }
            except:
                data['profil'] = None

        elif user.role == 'patient':
            try:
                profil = user.patient
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
                profil = user.responsable
                data['profil'] = {
                    "profil_id":   profil.id,
                    "departement": profil.departement,
                }
            except:
                data['profil'] = None

        return Response(data)


class RegisterResponsableView(generics.CreateAPIView):
    permission_classes = [IsResponsable]
    serializer_class = RegisterResponsableSerializer


class RegisterPatientView(generics.CreateAPIView):
    permission_classes = [IsResponsable]
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