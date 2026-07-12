from rest_framework import generics
from users.permissions import IsResponsable
from patients.models import ProfilPatient
from rendezvous.models import RendezVous
from .serializers import PatientRechercheSerializer, StatutPatientSerializer


class PatientRechercheView(generics.ListAPIView):
    """
    GET /api/responsables/patients/recherche/?q=<username>
    Recherche un patient existant par nom d'utilisateur (recherche partielle, insensible à la casse).
    """
    permission_classes = [IsResponsable]
    serializer_class = PatientRechercheSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q', '').strip()
        if not q:
            return ProfilPatient.objects.none()
        return ProfilPatient.objects.filter(
            user__username__icontains=q
        ).select_related('user')

class StatutPatientsView(generics.ListAPIView):
    permission_classes = [IsResponsable]
    serializer_class = StatutPatientSerializer

    def get_queryset(self):
        return ProfilPatient.objects.all().select_related('user')