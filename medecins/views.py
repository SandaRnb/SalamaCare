from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import ProfilMedecin
from .serializers import ProfilMedecinSerializer
from .services import (
    get_tous_les_medecins,
    get_medecin_par_id,
    creer_medecin,
    modifier_medecin,
    supprimer_medecin,
)


@require_http_methods(["GET"])
def liste_medecins(request):
    medecins   = get_tous_les_medecins()
    serializer = ProfilMedecinSerializer(medecins, many=True)
    return JsonResponse({"medecins": serializer.data})


@require_http_methods(["GET"])
def detail_medecin(request, medecin_id):
    medecin = get_medecin_par_id(medecin_id)

    if not medecin:
        return JsonResponse({"erreur": "Médecin introuvable"}, status=404)

    serializer = ProfilMedecinSerializer(medecin)
    return JsonResponse({"medecin": serializer.data})


@csrf_exempt
@require_http_methods(["POST"])
def creer_medecin_view(request):
    try:
        body      = json.loads(request.body)
        medecin   = creer_medecin(
            username   = body['username'],
            password   = body['password'],
            first_name = body.get('first_name', ''),
            last_name  = body.get('last_name', ''),
            email      = body.get('email', ''),
            specialite = body['specialite'],
            telephone  = body['telephone'],
        )
        serializer = ProfilMedecinSerializer(medecin)
        return JsonResponse({"message": "Médecin créé", "medecin": serializer.data}, status=201)

    except KeyError as e:
        return JsonResponse({"erreur": f"Champ manquant : {e}"}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def modifier_medecin_view(request, medecin_id):
    try:
        body    = json.loads(request.body)
        medecin = modifier_medecin(medecin_id, body)

        if not medecin:
            return JsonResponse({"erreur": "Médecin introuvable"}, status=404)

        serializer = ProfilMedecinSerializer(medecin)
        return JsonResponse({"message": "Médecin modifié", "medecin": serializer.data})

    except Exception as e:
        return JsonResponse({"erreur": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def supprimer_medecin_view(request, medecin_id):
    ok = supprimer_medecin(medecin_id)

    if not ok:
        return JsonResponse({"erreur": "Médecin introuvable"}, status=404)

    return JsonResponse({"message": "Médecin supprimé"})