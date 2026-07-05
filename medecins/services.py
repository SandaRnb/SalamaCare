from users.models import User
from .models import ProfilMedecin


def get_tous_les_medecins():
    return ProfilMedecin.objects.all()


def get_medecin_par_id(medecin_id):
    try:
        return ProfilMedecin.objects.get(id=medecin_id)
    except ProfilMedecin.DoesNotExist:
        return None


def creer_medecin(username, password, specialite, telephone,
                  first_name='', last_name='', email=''):
    # Crée le User d'abord
    user = User.objects.create_user(
        username   = username,
        password   = password,
        first_name = first_name,
        last_name  = last_name,
        email      = email,
        role       = 'medecin'
    )
    # Crée le profil lié
    return ProfilMedecin.objects.create(
        user       = user,
        specialite = specialite,
        telephone  = telephone,
    )


def modifier_medecin(medecin_id, data):
    try:
        medecin = ProfilMedecin.objects.get(id=medecin_id)
        medecin.specialite = data.get('specialite', medecin.specialite)
        medecin.telephone  = data.get('telephone',  medecin.telephone)
        medecin.save()
        return medecin
    except ProfilMedecin.DoesNotExist:
        return None


def supprimer_medecin(medecin_id):
    try:
        medecin = ProfilMedecin.objects.get(id=medecin_id)
        medecin.user.delete()  # supprime aussi le ProfilMedecin (CASCADE)
        return True
    except ProfilMedecin.DoesNotExist:
        return False