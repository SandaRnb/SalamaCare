# Fiche de suivi — Module Responsable (SalamaCARE)

**Dernière mise à jour :** 11 juillet 2026 (nuit)

---

## ✅ Fonctions terminées et testées

| # | Fonction | Endpoint | Sécurité | Statut |
|---|---|---|---|---|
| 1 | Rechercher un patient existant | `GET /api/responsables/patients/recherche/?q=` | `IsResponsable` | ✅ Testé OK |
| 2 | Créer un dossier patient | `POST /api/users/register/patient/` | `IsResponsable` (corrigé, était `AllowAny`) | ✅ Testé OK (201 / 401 sans token) |
| 3 | Créer un rendez-vous / attribuer patient à médecin | `POST /api/rendezvous/creer/` | `IsResponsable` (corrigé, était `IsAuthenticated`) | ✅ Testé OK (201 responsable / 403 patient) |

---

## 🔧 Corrections effectuées en cours de route (bugs trouvés et fixés)

1. `ProfilResponsable.user` et `ProfilMedecin.user` : `related_name` manquant → ajouté (`related_name='responsable'` / `'medecin'`)
2. App `consultations` : migrations jamais générées → générées et appliquées
3. `RegisterResponsableSerializer.departement` et `RegisterPatientSerializer` (date_naissance, adresse, telephone) : manquaient `write_only=True` → corrigé
4. `users/` : vues d'inscription (`RegisterResponsableView`, `RegisterPatientView`) et changement de mot de passe (`ChangePasswordView`) existaient en tant que serializers seuls, jamais reliées à des vues/urls → ajoutées
5. `RegisterPatientView` : permission `AllowAny` → changée en `IsResponsable` (un patient ne s'auto-inscrit pas, c'est le responsable qui l'enregistre)
6. `rendezvous/views.py` : `CreerRendezVousView` et `ModifierStatutView` étaient en `IsAuthenticated` (tout rôle) → changées en `IsResponsable`, conformément au cahier des charges (le responsable gère les rendez-vous, pas le médecin)
7. `DetailRendezVousView.delete()` : ajout d'une vérification manuelle `role == 'responsable'` (le `GET` reste ouvert à tous, le `DELETE` restreint)

---

## ⏳ Fonctions restantes à faire

| Fonction | Endpoint prévu | Remarque |
|---|---|---|
| Reporter un rendez-vous | *(non couvert actuellement)* | `ModifierStatutView` ne gère que le `statut`, pas `date_heure` — à voir si on étend ce serializer ou on ignore pour le MVP |
| Annuler un rendez-vous | `PUT /api/rendezvous/<id>/statut/` (statut=annule) | Déjà existant via `ModifierStatutView` — **à vérifier si la permission `IsResponsable` y est bien appliquée** (fait hier soir, à re-tester) |
| Lister l'agenda / rendez-vous | `GET /api/rendezvous/` | Existe (`IsAuthenticated`) — à décider si on restreint plus (ex: un responsable voit tout, un médecin voit les siens) |
| Envoyer une notification à un médecin | *(à définir)* | App `notifications` pas encore vue |
| Voir le statut des patients | *(à définir)* | À clarifier : vient d'un champ sur `ProfilPatient` ou déduit du `statut` des `RendezVous`/`Consultation` ? |
| (Bonus) Tableau de bord | *(non prioritaire)* | Nombre de patients du jour |

### ❌ Retiré de la liste

- **Assigner une consultation** — retiré. Analyse du document projet (PDF "MVC procédées", scénario principal p.7) confirme que c'est **le médecin** qui remplit/crée la consultation, pas le responsable. Le code déjà écrit dans `consultations/views.py` (permission `IsMedecin` sur create/update) est cohérent avec ce document. Le responsable garde seulement un accès en lecture (`IsMedecinOrResponsable` sur les GET), déjà couvert par l'app existante — rien à développer côté responsable.
- Bug signalé au collaborateur en charge de `consultations` : `user.profilmedecin` devrait être `user.medecin` dans `ConsultationListView.get()` (incohérent avec le `related_name` corrigé sur `ProfilMedecin`).

---

## 📌 Points à vérifier au prochain démarrage

- Retester `ModifierStatutView` avec un token responsable ET un token non-responsable (comme fait pour `creer/`), pour confirmer que la permission appliquée hier fonctionne.
- Explorer `consultations/models.py`, `serializers.py`, `views.py` (pas encore vus) avant de coder "assigner une consultation".
- Explorer l'app `notifications` (pas encore vue du tout) avant de coder "envoyer une notification".
- Clarifier avec l'équipe la logique de "statut du patient" (en attente / en consultation / terminé) : champ dédié ou déduit ?
