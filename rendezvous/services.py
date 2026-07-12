from .models import RendezVous
from medecins.models import ProfilMedecin
from patients.models import ProfilPatient


def get_tous_les_rendezvous():
    return RendezVous.objects.all()


def get_rendezvous_par_id(rdv_id):
    try:
        return RendezVous.objects.get(id=rdv_id)
    except RendezVous.DoesNotExist:
        return None


def get_rendezvous_par_patient(patient_id):
    """Tous les RDV d'un patient"""
    return RendezVous.objects.filter(patient__id=patient_id)


def get_rendezvous_par_medecin(medecin_id):
    """Tous les RDV d'un médecin"""
    return RendezVous.objects.filter(medecin__id=medecin_id)


def creer_rendezvous(patient_id, medecin_id, date_heure, motif):
    """Crée un nouveau rendez-vous"""
    try:
        patient = ProfilPatient.objects.get(id=patient_id)
        medecin = ProfilMedecin.objects.get(id=medecin_id)
    except ProfilPatient.DoesNotExist:
        return None, "Patient introuvable"
    except ProfilMedecin.DoesNotExist:
        return None, "Médecin introuvable"

    # Vérifier si le médecin a déjà un RDV à cette heure
    conflit = RendezVous.objects.filter(
        medecin    = medecin,
        date_heure = date_heure,
        statut__in = ['en_attente', 'confirme']
    ).exists()

    if conflit:
        return None, "Le médecin a déjà un rendez-vous à cette heure"

    rdv = RendezVous.objects.create(
        patient    = patient,
        medecin    = medecin,
        date_heure = date_heure,
        motif      = motif,
    )
    return rdv, None


def modifier_statut(rdv_id, nouveau_statut):
    """Change le statut d'un RDV"""
    try:
        rdv        = RendezVous.objects.get(id=rdv_id)
        rdv.statut = nouveau_statut
        rdv.save()
        return rdv
    except RendezVous.DoesNotExist:
        return None


def annuler_rendezvous(rdv_id):
    """Annule un RDV"""
    return modifier_statut(rdv_id, RendezVous.Statut.ANNULE)

def reporter_rendezvous(rdv_id, nouvelle_date_heure):
    """Change la date/heure d'un RDV (report)"""
    try:
        rdv = RendezVous.objects.get(id=rdv_id)

        # Vérifier conflit avec le même médecin à la nouvelle date
        conflit = RendezVous.objects.filter(
            medecin    = rdv.medecin,
            date_heure = nouvelle_date_heure,
            statut__in = ['en_attente', 'confirme']
        ).exclude(id=rdv_id).exists()

        if conflit:
            return None, "Le médecin a déjà un rendez-vous à cette heure"

        rdv.date_heure = nouvelle_date_heure
        rdv.save()
        return rdv, None
    except RendezVous.DoesNotExist:
        return None, "RDV introuvable"


def supprimer_rendezvous(rdv_id):
    try:
        rdv = RendezVous.objects.get(id=rdv_id)
        rdv.delete()
        return True
    except RendezVous.DoesNotExist:
        return False