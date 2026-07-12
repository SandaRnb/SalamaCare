from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsResponsable

from .models import RendezVous
from .serializers import (
    RendezVousSerializer,
    CreerRendezVousSerializer,
    ModifierStatutSerializer,
)

from . import services
from .services import (
    get_tous_les_rendezvous,
    get_rendezvous_par_id,
    get_rendezvous_par_patient,
    get_rendezvous_par_medecin,
    creer_rendezvous,
    modifier_statut,
    annuler_rendezvous,
    supprimer_rendezvous,
)

# ── Liste tous les RDV ────────────────────────────────────
class ListeRendezVousView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'responsable':
            rdvs = get_tous_les_rendezvous()
        elif user.role == 'medecin':
            rdvs = get_rendezvous_par_medecin(user.medecin.id)
        elif user.role == 'patient':
            rdvs = get_rendezvous_par_patient(user.patient.id)
        else:
            rdvs = RendezVous.objects.none()

        serializer = RendezVousSerializer(rdvs, many=True)
        return Response({"rendezvous": serializer.data})

# ── Créer un RDV ──────────────────────────────────────────
class CreerRendezVousView(APIView):
    permission_classes = [IsResponsable]

    def post(self, request):
        serializer = CreerRendezVousSerializer(data=request.data)
        if serializer.is_valid():
            rdv, erreur = creer_rendezvous(
                patient_id = serializer.validated_data['patient_id'],
                medecin_id = serializer.validated_data['medecin_id'],
                date_heure = serializer.validated_data['date_heure'],
                motif      = serializer.validated_data['motif'],
            )
            if erreur:
                return Response({"erreur": erreur}, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {"message": "Rendez-vous créé", "rendezvous": RendezVousSerializer(rdv).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Détail / Annuler / Supprimer ──────────────────────────
class DetailRendezVousView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, rdv_id):
        rdv = get_rendezvous_par_id(rdv_id)
        if not rdv:
            return Response({"erreur": "RDV introuvable"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RendezVousSerializer(rdv)
        return Response({"rendezvous": serializer.data})

    def delete(self, request, rdv_id):
        if request.user.role != 'responsable':
            return Response({"erreur": "Seul un responsable peut supprimer un rendez-vous"}, status=status.HTTP_403_FORBIDDEN)
        ok = supprimer_rendezvous(rdv_id)
        if not ok:
            return Response({"erreur": "RDV introuvable"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Rendez-vous supprimé"})


# ── Modifier statut ───────────────────────────────────────
class ModifierStatutView(APIView):
    permission_classes = [IsResponsable]

    def put(self, request, rdv_id):
        serializer = ModifierStatutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Cas : report de date
        if 'date_heure' in data:
            rdv, erreur = services.reporter_rendezvous(rdv_id, data['date_heure'])
            if erreur:
                return Response({"erreur": erreur}, status=status.HTTP_400_BAD_REQUEST)

        # Cas : changement de statut
        if 'statut' in data:
            rdv = modifier_statut(rdv_id, data['statut'])
            if not rdv:
                return Response({"erreur": "RDV introuvable"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "message": "Rendez-vous modifié",
            "rendezvous": RendezVousSerializer(rdv).data
        })

# ── RDV par patient ───────────────────────────────────────
class RendezVousPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        rdvs       = get_rendezvous_par_patient(patient_id)
        serializer = RendezVousSerializer(rdvs, many=True)
        return Response({"rendezvous": serializer.data})


# ── RDV par médecin ───────────────────────────────────────
class RendezVousMedecinView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, medecin_id):
        rdvs       = get_rendezvous_par_medecin(medecin_id)
        serializer = RendezVousSerializer(rdvs, many=True)
        return Response({"rendezvous": serializer.data})