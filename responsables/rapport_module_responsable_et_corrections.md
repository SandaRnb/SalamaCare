# Rapport — Module Responsable & corrections transverses

**Auteur :** Johan (module Responsable)
**Période :** 10–12 juillet 2026
**Contexte :** Développement complet des fonctions du module Responsable, avec vérification et correction de plusieurs bugs découverts dans les apps `users`, `medecins`, `rendezvous`, `consultations`, `notifications` en cours de route.

---

## 1. Fonctions développées dans le module Responsable

Toutes testées de bout en bout via Postman (token JWT + vérification en base après chaque action).

| # | Fonction | Endpoint | Sécurité |
|---|---|---|---|
| 1 | Rechercher un patient existant | `GET /api/responsables/patients/recherche/?q=` | `IsResponsable` |
| 2 | Créer un dossier patient | `POST /api/users/register/patient/` | `IsResponsable` |
| 3 | Créer un rendez-vous / attribuer patient à médecin | `POST /api/rendezvous/creer/` | `IsResponsable` |
| 4 | Annuler un rendez-vous | `PUT /api/rendezvous/<id>/statut/` (statut=annule) | `IsResponsable` |
| 5 | Reporter un rendez-vous | `PUT /api/rendezvous/<id>/statut/` (date_heure=...) | `IsResponsable` |
| 6 | Lister l'agenda | `GET /api/rendezvous/` | `IsAuthenticated`, filtré par rôle |
| 7 | Envoyer une notification à un médecin | `POST /api/notifications/envoyer/` | `IsResponsable` |
| 8 | Voir le statut des patients | `GET /api/responsables/patients/statut/` | `IsResponsable` |

**Fonction retirée du périmètre responsable :** *"Assigner une consultation"* — après analyse du document projet (scénario métier officiel), c'est le médecin qui remplit/crée la consultation, pas le responsable. Le code déjà existant dans `consultations/` (permission `IsMedecin` sur la création) est cohérent avec ce choix. Le responsable garde un accès en lecture seule sur les consultations (déjà couvert par `IsMedecinOrResponsable` existant, rien à développer côté responsable).

**Fonction bonus non traitée :** tableau de bord (nombre de patients du jour) — non prioritaire, laissée de côté pour se concentrer sur le cœur de fonction.

---

## 2. Fichiers créés/modifiés dans `responsables/`

- `responsables/models.py` — `ProfilResponsable` (correction `related_name`, voir section 3)
- `responsables/serializers.py` — `PatientRechercheSerializer`, `StatutPatientSerializer`
- `responsables/views.py` — `PatientRechercheView`, `StatutPatientsView`
- `responsables/urls.py` — routes `patients/recherche/`, `patients/statut/`

Les autres fonctions (2, 3, 4, 5, 6, 7) réutilisent des endpoints déjà présents dans `users/`, `rendezvous/`, `notifications/` — pas de duplication de code, seulement des ajustements de permissions pour restreindre l'accès au rôle responsable là où c'était trop ouvert.

---

## 3. Bugs trouvés et corrigés dans les autres apps

### 3.1 `related_name` manquant sur les profils (`responsables`, `medecins`)
`MyLoginView` (dans `users/`) utilise `user.medecin`, `user.patient`, `user.responsable` pour récupérer le profil du user connecté. Ces raccourcis nécessitent un `related_name` explicite sur le `OneToOneField`.
- `ProfilResponsable.user` : `related_name` absent → ajouté `related_name='responsable'`
- `ProfilMedecin.user` : `related_name` absent → ajouté `related_name='medecin'`
- `ProfilPatient.user` : déjà correct dès le départ

**Impact avant correction :** connexion de tout médecin/responsable renvoyait `profil: None` silencieusement.

### 3.2 Migrations manquantes (`consultations`, `notifications`)
Deux apps avaient leur modèle écrit dans le code mais **aucune migration générée ni appliquée** — tables absentes en base MySQL. Découvert lors de tests de suppression en cascade et lors du premier test d'envoi de notification (`ProgrammingError: table doesn't exist`).
→ `makemigrations` + `migrate` effectués pour les deux apps.

### 3.3 Serializers d'inscription : champs non-modèle sans `write_only=True`
`RegisterResponsableSerializer.departement` et `RegisterPatientSerializer.date_naissance/adresse/telephone` sont des champs qui n'existent pas sur le modèle `User` (ils appartiennent aux profils liés). Sans `write_only=True`, DRF plante en tentant de les lire depuis l'instance `User`.
→ `write_only=True` ajouté sur ces 4 champs.

### 3.4 Vues d'inscription/changement mdp absentes de `users/`
Les serializers (`RegisterResponsableSerializer`, `RegisterPatientSerializer`, `ChangePasswordSerializer`) existaient mais n'étaient reliés à aucune vue ni route. Impossible de créer un compte via l'API.
→ Ajout de `RegisterResponsableView`, `RegisterPatientView`, `ChangePasswordView` + routes correspondantes dans `users/urls.py`.

### 3.5 Permissions trop ouvertes
- `RegisterPatientView` était en `AllowAny` (n'importe qui peut créer un patient) → changé en `IsResponsable`, cohérent avec le fait qu'un patient ne s'auto-inscrit pas, c'est le responsable qui l'enregistre à l'accueil.
- `CreerRendezVousView` et `ModifierStatutView` (dans `rendezvous/`) étaient en `IsAuthenticated` (tout rôle confondu) → changées en `IsResponsable`, conformément au document projet officiel (le responsable gère les rendez-vous, pas le médecin ni le patient directement).
- `DetailRendezVousView.delete()` : ajout d'une vérification manuelle du rôle (le `GET` reste ouvert à tous les rôles connectés, seul le `DELETE` est restreint responsable).

### 3.6 `ListeRendezVousView` : filtrage par rôle ajouté
À l'origine ouverte à tout `IsAuthenticated` sans filtrage : n'importe quel utilisateur connecté voyait **tous** les rendez-vous de tout le monde. Corrigé pour que :
- Le responsable voit tous les RDV
- Un médecin ne voit que ses propres RDV
- Un patient ne voit que ses propres RDV

### 3.7 Bug signalé (non corrigé par nous, hors périmètre) : `consultations/views.py`
`ConsultationListView.get()` utilise `user.profilmedecin` au lieu de `user.medecin` (incohérent avec le `related_name` corrigé en 3.1). Signalé au collaborateur responsable de l'app `consultations`.

### 3.8 Conflits Git non résolus (fusion de branches)
À plusieurs reprises après un merge avec la branche `origin/natha-feature`, des fichiers contenaient encore les marqueurs de conflit Git (`<<<<<<< HEAD`, `=======`, `>>>>>>>`) non résolus, empêchant le serveur de démarrer :
- `consultations/migrations/0001_initial.py`
- `users/urls.py`
- `users/views.py` (mélange incohérent de deux implémentations de vues de connexion/profil, avec des imports manquants comme `LoginSerializer`, `RefreshToken`)

Résolus en conservant la version cohérente avec le reste du projet déjà testé (HEAD), en reconstruisant proprement le fichier là où le merge avait mélangé du code de façon syntaxiquement invalide.

**Recommandation à l'équipe :** faire une recherche globale de `<<<<<<< HEAD` dans tout le projet après chaque merge, avant de tester, pour éviter de perdre du temps à diagnostiquer des erreurs qui sont en réalité de simples conflits non résolus.

### 3.9 Erreurs de configuration (`config/settings.py`, `config/urls.py`)
- `BASE_DIR = Path(_file_)` → faute de frappe, corrigé en `Path(__file__)`
- App `'responsables'` absente de `INSTALLED_APPS` → ajoutée
- Route `path('api/notifications/', include('notifications.urls'))` laissée commentée → décommentée

---

## 4. Points positifs constatés côté configuration

Le collaborateur en charge de `users`/`settings` a corrigé de façon proactive, suite à l'analyse qu'on avait partagée sur la compatibilité avec le frontend :
- `CORS_ALLOWED_ORIGINS` configuré pour le front React (`localhost:3000`)
- Durée de vie de l'access token JWT passée à 30 minutes (au lieu de 5 min par défaut), pour correspondre au besoin du frontend (stockage `localStorage`, pas de refresh automatique visible)

---

## 5. Points encore ouverts / à surveiller

- **Format de réponse du login** attendu par le front (`{"token": ..., "user": {"role": ...}}`) ne correspond pas encore à la réponse actuelle de `/api/token/` (`{"access": ..., "refresh": ...}`). Nécessite une vue de login personnalisée si on veut respecter exactement le contrat attendu par le front (voir `LOGIN_EXPECTATIONS.md` fourni par l'équipe front).
- **Authentification par email vs username** : le front veut envoyer `email`, le backend authentifie actuellement par `username`. À trancher avec l'équipe.
- **`RegisterResponsableView` est maintenant en `IsResponsable`** (changé par un collaborateur pendant un merge) — cela bloque la toute première création de compte responsable puisque personne n'est responsable au départ. À clarifier : faut-il un compte admin/superuser initial créé manuellement (`createsuperuser` ou fixture), ou remettre `AllowAny` pour cette route spécifique ?
- Fonction bonus "tableau de bord" non développée (non prioritaire).
