from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ProfilPatientSerializer, RegisterPatientSerializer
from .services import (
    get_tous_les_patients,
    get_patient_par_id,
    modifier_patient,
    supprimer_patient,
)


# ── Inscription ───────────────────────────────────────────
class RegisterPatientView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterPatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Patient créé avec succès"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Liste ─────────────────────────────────────────────────
class ListePatientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients   = get_tous_les_patients()
        serializer = ProfilPatientSerializer(patients, many=True)
        return Response({"patients": serializer.data})


# ── Détail / Modification / Suppression ───────────────────
class DetailPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_patient_par_id(patient_id)
        if not patient:
            return Response(
                {"erreur": "Patient introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProfilPatientSerializer(patient)
        return Response({"patient": serializer.data})

    def put(self, request, patient_id):
        patient = modifier_patient(patient_id, request.data)
        if not patient:
            return Response(
                {"erreur": "Patient introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProfilPatientSerializer(patient)
        return Response({
            "message": "Patient modifié",
            "patient": serializer.data
        })

    def delete(self, request, patient_id):
        ok = supprimer_patient(patient_id)
        if not ok:
            return Response(
                {"erreur": "Patient introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({"message": "Patient supprimé"})