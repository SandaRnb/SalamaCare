from rest_framework.views import APIView
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework.permissions import AllowAny, IsAuthenticated

#ajout d'import
from rest_framework import generics, status
from .serializers import (
    RegisterResponsableSerializer,
    RegisterPatientSerializer,
    ChangePasswordSerializer,
)
from users.permissions import IsResponsable
=======
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer
>>>>>>> origin/natha-feature


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
<<<<<<< HEAD
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
    permission_classes = [IsResponsable]  # ← Seul un responsable ou un admin peut créer un autre responsable
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
=======
            "profil":   profil,
        })
>>>>>>> origin/natha-feature
