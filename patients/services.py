from .models import ProfilPatient


def get_tous_les_patients():
    return ProfilPatient.objects.all()


def get_patient_par_id(patient_id):
    try:
        return ProfilPatient.objects.get(id=patient_id)
    except ProfilPatient.DoesNotExist:
        return None


def modifier_patient(patient_id, data):
    try:
        patient = ProfilPatient.objects.get(id=patient_id)
        patient.adresse        = data.get('adresse',        patient.adresse)
        patient.telephone      = data.get('telephone',      patient.telephone)
        patient.date_naissance = data.get('date_naissance', patient.date_naissance)
        patient.save()
        return patient
    except ProfilPatient.DoesNotExist:
        return None


def supprimer_patient(patient_id):
    try:
        patient = ProfilPatient.objects.get(id=patient_id)
        patient.user.delete()
        return True
    except ProfilPatient.DoesNotExist:
        return False