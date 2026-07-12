from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user    = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            # Construire le profil selon le role
            profil = {}
            if user.role == 'medecin':
                try:
                    profil = {
                        "profil_id":  user.medecin.id,
                        "specialite": user.medecin.specialite,
                        "telephone":  user.medecin.telephone,
                    }
                except: pass

            elif user.role == 'patient':
                try:
                    profil = {
                        "profil_id":      user.patient.id,
                        "date_naissance": str(user.patient.date_naissance),
                        "adresse":        user.patient.adresse,
                        "telephone":      user.patient.telephone,
                    }
                except: pass

            elif user.role == 'responsable':
                try:
                    profil = {
                        "profil_id":   user.responsable.id,
                        "departement": user.responsable.departement,
                    }
                except: pass

            return Response({
                "access":  str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id":       user.id,
                    "username": user.username,
                    "email":    user.email,
                    "role":     user.role,
                    "profil":   profil,
                }
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonProfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user  = request.user
        profil = {}

        if user.role == 'medecin':
            try:
                profil = {
                    "profil_id":  user.medecin.id,
                    "specialite": user.medecin.specialite,
                    "telephone":  user.medecin.telephone,
                }
            except: pass

        elif user.role == 'patient':
            try:
                profil = {
                    "profil_id":      user.patient.id,
                    "date_naissance": str(user.patient.date_naissance),
                    "adresse":        user.patient.adresse,
                    "telephone":      user.patient.telephone,
                }
            except: pass

        elif user.role == 'responsable':
            try:
                profil = {
                    "profil_id":   user.responsable.id,
                    "departement": user.responsable.departement,
                }
            except: pass

        return Response({
            "id":       user.id,
            "username": user.username,
            "email":    user.email,
            "role":     user.role,
            "profil":   profil,
        })