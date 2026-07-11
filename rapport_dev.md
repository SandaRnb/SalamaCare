## Rapport — Corrections post-merge (branche natha-feature)

**Contexte :** vérification de la cohérence entre `users/views.py` (MyLoginView) et les modèles de profils avant développement de `responsable/views.py`.

### Bugs identifiés et corrigés

| App           | Fichier | Problème | Correction |
|---            |---|---|---|
| `responsables`| `models.py` | `OneToOneField` sans `related_name` → `user.responsable` cassait le login           | Ajout `related_name='responsable'` |
| `medecins`    | `models.py` | Même bug → `user.medecin` cassait le login | Ajout `related_name='medecin'` |
| `patients` | `models.py` | ✅ Déjà correct (`related_name='patient'`) | Aucune |
| `consultations` | — | Aucune migration n'existait (table absente en base) | `makemigrations` + `migrate` exécutés |

### Migrations appliquées
- `responsables.0002_alter_profilresponsable_user`
- `medecins.0002_alter_profilmedecin_user`
- `patients.0002_alter_profilpatient_options_alter_profilpatient_user`
- `consultations.0001_initial` (création tables `Consultation`, `Ordonnance`)

### Tests de validation effectués
- Création `User` + profil pour `responsable` et `medecin` → relation inverse (`u.responsable`, `u.medecin`) fonctionnelle
- Suppression en cascade testée et propre

### État actuel
Base de données saine, les 3 profils (`Patient`, `Medecin`, `Responsable`) sont correctement liés à `User` et exploitables via `MyLoginView`. Prêt pour développement de `responsable/views.py`.

