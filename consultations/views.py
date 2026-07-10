from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.permissions import IsMedecin, IsResponsable, IsMedecinOrResponsable
from .models import Consultation, Ordonnance
from .serializers import (
    ConsultationSerializer,
    ConsultationCreateSerializer,
    ConsultationUpdateSerializer,
    OrdonnanceSerializer
)
from . import services


# ─── Liste + Création ─────────────────────────────────────────
class ConsultationListView(APIView):

    def get_permissions(self):
        # GET → médecin ou responsable
        # POST → médecin seulement
        if self.request.method == "POST":
            return [IsMedecin()]
        return [IsMedecinOrResponsable()]

    def get(self, request):
        user = request.user

        # médecin → voit ses propres consultations
        if user.role == "medecin":
            consultations = services.get_consultations_medecin(
                user.profilmedecin
            )

        # responsable → voit toutes les consultations
        else:
            consultations = services.get_all_consultations()

        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsultationCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ─── Détail + Modification ────────────────────────────────────
class ConsultationDetailView(APIView):
    permission_classes = [IsMedecinOrResponsable]

    def get_object(self, pk):
        consultation = services.get_consultation_by_id(pk)
        if consultation is None:
            return None
        return consultation

    def get(self, request, pk):
        consultation = self.get_object(pk)
        if consultation is None:
            return Response(
                {"error": "Consultation introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ConsultationSerializer(consultation)
        return Response(serializer.data)

    def put(self, request, pk):
        # seul le médecin peut modifier
        if request.user.role != "medecin":
            return Response(
                {"error": "Seul le médecin peut modifier une consultation."},
                status=status.HTTP_403_FORBIDDEN
            )

        consultation = self.get_object(pk)
        if consultation is None:
            return Response(
                {"error": "Consultation introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ConsultationUpdateSerializer(
            consultation,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ─── Consultations d'un patient ───────────────────────────────
class ConsultationPatientView(APIView):
    permission_classes = [IsMedecinOrResponsable]

    def get(self, request, patient_id):
        from patients.models import ProfilPatient
        try:
            patient = ProfilPatient.objects.get(id=patient_id)
        except ProfilPatient.DoesNotExist:
            return Response(
                {"error": "Patient introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        consultations = services.get_consultations_patient(patient)
        serializer    = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)


# ─── Ordonnances d'une consultation ──────────────────────────
class OrdonnanceListView(APIView):
    permission_classes = [IsMedecinOrResponsable]

    def get(self, request, consultation_id):
        try:
            consultation = Consultation.objects.get(id=consultation_id)
        except Consultation.DoesNotExist:
            return Response(
                {"error": "Consultation introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        ordonnances = consultation.ordonnances.all()
        serializer  = OrdonnanceSerializer(ordonnances, many=True)
        return Response(serializer.data)

    def post(self, request, consultation_id):
        if request.user.role != "medecin":
            return Response(
                {"error": "Seul le médecin peut ajouter une ordonnance."},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            consultation = Consultation.objects.get(id=consultation_id)
        except Consultation.DoesNotExist:
            return Response(
                {"error": "Consultation introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrdonnanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ─── Supprimer une ordonnance ─────────────────────────────────
class OrdonnanceDeleteView(APIView):
    permission_classes = [IsMedecin]

    def delete(self, request, pk):
        supprime = services.supprimer_ordonnance(pk)
        if supprime:
            return Response(
                {"message": "Ordonnance supprimée."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "Ordonnance introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )
