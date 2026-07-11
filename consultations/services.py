from .models import Consultation, Ordonnance
from rendezvous.models import RendezVous


def get_toutes_les_consultations():
    return Consultation.objects.all()


def get_consultation_par_id(consultation_id):
    try:
        return Consultation.objects.get(id=consultation_id)
    except Consultation.DoesNotExist:
        return None


def get_consultations_par_patient(patient_id):
    return Consultation.objects.filter(patient__id=patient_id)


def get_consultations_par_medecin(medecin_id):
    return Consultation.objects.filter(medecin__id=medecin_id)


def creer_consultation(rdv_id, diagnostic, traitement='', notes=''):
    """Crée une consultation à partir d'un RDV existant"""
    try:
        rdv = RendezVous.objects.get(id=rdv_id)
    except RendezVous.DoesNotExist:
        return None, "Rendez-vous introuvable"

    # Vérifier si une consultation existe déjà pour ce RDV
    if hasattr(rdv, 'consultation'):
        return None, "Une consultation existe déjà pour ce rendez-vous"

    consultation = Consultation.objects.create(
        rendez_vous = rdv,
        patient     = rdv.patient,
        medecin     = rdv.medecin,
        diagnostic  = diagnostic,
        traitement  = traitement,
        notes       = notes,
    )

    # Marquer le RDV comme terminé automatiquement
    rdv.statut = 'termine'
    rdv.save()

    return consultation, None


def modifier_consultation(consultation_id, data):
    try:
        consultation            = Consultation.objects.get(id=consultation_id)
        consultation.diagnostic = data.get('diagnostic', consultation.diagnostic)
        consultation.traitement = data.get('traitement', consultation.traitement)
        consultation.notes      = data.get('notes',      consultation.notes)
        consultation.save()
        return consultation
    except Consultation.DoesNotExist:
        return None


def supprimer_consultation(consultation_id):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
        consultation.delete()
        return True
    except Consultation.DoesNotExist:
        return False


# ── Ordonnances ───────────────────────────────────────────

def ajouter_ordonnance(consultation_id, medicament, posologie, duree):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
        return Ordonnance.objects.create(
            consultation = consultation,
            medicament   = medicament,
            posologie    = posologie,
            duree        = duree,
        ), None
    except Consultation.DoesNotExist:
        return None, "Consultation introuvable"


def supprimer_ordonnance(ordonnance_id):
    try:
        ordonnance = Ordonnance.objects.get(id=ordonnance_id)
        ordonnance.delete()
        return True
    except Ordonnance.DoesNotExist:
        return False