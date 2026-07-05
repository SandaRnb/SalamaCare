from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ProfilMedecinSerializer, RegisterMedecinSerializer
from .services import (
    get_tous_les_medecins,
    get_medecin_par_id,
    modifier_medecin,
    supprimer_medecin,
)


# ── Inscription ───────────────────────────────────────────
class RegisterMedecinView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterMedecinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Médecin créé avec succès"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Liste ─────────────────────────────────────────────────
class ListeMedecinsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        medecins   = get_tous_les_medecins()
        serializer = ProfilMedecinSerializer(medecins, many=True)
        return Response({"medecins": serializer.data})


# ── Détail / Modification / Suppression ───────────────────
class DetailMedecinView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, medecin_id):
        medecin = get_medecin_par_id(medecin_id)
        if not medecin:
            return Response(
                {"erreur": "Médecin introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProfilMedecinSerializer(medecin)
        return Response({"medecin": serializer.data})

    def put(self, request, medecin_id):
        medecin = modifier_medecin(medecin_id, request.data)
        if not medecin:
            return Response(
                {"erreur": "Médecin introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProfilMedecinSerializer(medecin)
        return Response({
            "message": "Médecin modifié",
            "medecin": serializer.data
        })

    def delete(self, request, medecin_id):
        ok = supprimer_medecin(medecin_id)
        if not ok:
            return Response(
                {"erreur": "Médecin introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({"message": "Médecin supprimé"})