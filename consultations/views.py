from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ConsultationSerializer,
    CreerConsultationSerializer,
    AjouterOrdonnanceSerializer,
)
from .services import (
    get_toutes_les_consultations,
    get_consultation_par_id,
    get_consultations_par_patient,
    get_consultations_par_medecin,
    creer_consultation,
    modifier_consultation,
    supprimer_consultation,
    ajouter_ordonnance,
    supprimer_ordonnance,
)


class ListeConsultationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        consultations = get_toutes_les_consultations()
        serializer    = ConsultationSerializer(consultations, many=True)
        return Response({"consultations": serializer.data})


class CreerConsultationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreerConsultationSerializer(data=request.data)
        if serializer.is_valid():
            consultation, erreur = creer_consultation(
                rdv_id     = serializer.validated_data['rdv_id'],
                diagnostic = serializer.validated_data['diagnostic'],
                traitement = serializer.validated_data['traitement'],
                notes      = serializer.validated_data['notes'],
            )
            if erreur:
                return Response({"erreur": erreur}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {"message": "Consultation créée", "consultation": ConsultationSerializer(consultation).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailConsultationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, consultation_id):
        consultation = get_consultation_par_id(consultation_id)
        if not consultation:
            return Response({"erreur": "Consultation introuvable"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConsultationSerializer(consultation)
        return Response({"consultation": serializer.data})

    def put(self, request, consultation_id):
        consultation = modifier_consultation(consultation_id, request.data)
        if not consultation:
            return Response({"erreur": "Consultation introuvable"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConsultationSerializer(consultation)
        return Response({"message": "Consultation modifiée", "consultation": serializer.data})

    def delete(self, request, consultation_id):
        ok = supprimer_consultation(consultation_id)
        if not ok:
            return Response({"erreur": "Consultation introuvable"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Consultation supprimée"})


class ConsultationsPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        consultations = get_consultations_par_patient(patient_id)
        serializer    = ConsultationSerializer(consultations, many=True)
        return Response({"consultations": serializer.data})


class ConsultationsMedecinView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, medecin_id):
        consultations = get_consultations_par_medecin(medecin_id)
        serializer    = ConsultationSerializer(consultations, many=True)
        return Response({"consultations": serializer.data})


class OrdonnanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, consultation_id):
        serializer = AjouterOrdonnanceSerializer(data=request.data)
        if serializer.is_valid():
            ordonnance, erreur = ajouter_ordonnance(
                consultation_id = consultation_id,
                medicament      = serializer.validated_data['medicament'],
                posologie       = serializer.validated_data['posologie'],
                duree           = serializer.validated_data['duree'],
            )
            if erreur:
                return Response({"erreur": erreur}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Ordonnance ajoutée"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, consultation_id, ordonnance_id):
        ok = supprimer_ordonnance(ordonnance_id)
        if not ok:
            return Response({"erreur": "Ordonnance introuvable"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Ordonnance supprimée"})