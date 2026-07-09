from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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