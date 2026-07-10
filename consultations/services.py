from .models import Consultation, Ordonnance


# ─── Créer une consultation ───────────────────────────────────
def creer_consultation(rendez_vous, patient, medecin,
                       diagnostic, traitement="", notes=""):
    # vérifier si consultation déjà existante
    if Consultation.objects.filter(rendez_vous=rendez_vous).exists():
        raise ValueError(
            "Une consultation existe déjà pour ce rendez-vous."
        )

    consultation = Consultation.objects.create(
        rendez_vous = rendez_vous,
        patient     = patient,
        medecin     = medecin,
        diagnostic  = diagnostic,
        traitement  = traitement,
        notes       = notes
    )
    return consultation


# ─── Ajouter une ordonnance ───────────────────────────────────
def ajouter_ordonnance(consultation, medicament, posologie, duree):
    ordonnance = Ordonnance.objects.create(
        consultation = consultation,
        medicament   = medicament,
        posologie    = posologie,
        duree        = duree
    )
    return ordonnance


# ─── Récupérer consultations d'un patient ─────────────────────
def get_consultations_patient(patient):
    return Consultation.objects.filter(
        patient=patient
    ).order_by("-created_at")


# ─── Récupérer consultations d'un médecin ─────────────────────
def get_consultations_medecin(medecin):
    return Consultation.objects.filter(
        medecin=medecin
    ).order_by("-created_at")


# ─── Récupérer toutes les consultations ───────────────────────
def get_all_consultations():
    return Consultation.objects.all().order_by("-created_at")


# ─── Récupérer une consultation par id ────────────────────────
def get_consultation_by_id(consultation_id):
    try:
        return Consultation.objects.get(id=consultation_id)
    except Consultation.DoesNotExist:
        return None


# ─── Modifier une consultation ────────────────────────────────
def modifier_consultation(consultation, diagnostic=None,
                          traitement=None, notes=None):
    if diagnostic is not None:
        consultation.diagnostic = diagnostic
    if traitement is not None:
        consultation.traitement = traitement
    if notes is not None:
        consultation.notes = notes
    consultation.save()
    return consultation


# ─── Supprimer une ordonnance ─────────────────────────────────
def supprimer_ordonnance(ordonnance_id):
    try:
        ordonnance = Ordonnance.objects.get(id=ordonnance_id)
        ordonnance.delete()
        return True
    except Ordonnance.DoesNotExist:
        return False