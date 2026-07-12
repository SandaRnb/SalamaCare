salamacare_api/
│
├── users/
│   └── models.py
│       ├── User
│       ├── ProfilMedecin
│       ├── ProfilPatient
│       └── ProfilResponsable
│
├── patients/
│   └── models.py
│       └── DossierPatient
│           ├── patient      FK → User
│           ├── groupe_sanguin
│           ├── antecedents
│           ├── allergies
│           └── date_creation
│
├── medecins/
│   └── models.py
│       └── Disponibilite
│           ├── medecin      FK → User
│           ├── jour
│           ├── heure_debut
│           └── heure_fin
│
├── rendezvous/
│   └── models.py
│       └── RendezVous
│           ├── patient      FK → User
│           ├── medecin      FK → User
│           ├── date
│           ├── heure
│           ├── motif
│           └── statut
│
├── consultations/
│   └── models.py
│       └── Consultation
│           ├── rendezvous   FK → RendezVous
│           ├── diagnostic
│           ├── ordonnance
│           ├── notes
│           └── date
│
└── notifications/
    └── models.py
        └── Notification
            ├── destinataire FK → User
            ├── rendezvous   FK → RendezVous
            ├── message
            ├── type
            ├── lu
            └── date_envoi



=== LOGIQUE ET DEPENDANCES ===

users/          → qui peut se connecter ? 
→ User + ProfilMedecin + ProfilPatient + ProfilResponsable → tokens JWT + permissions → aucune dépendance vers les autres apps

patients/       → informations médicales du patient 
→ dossier patient, antécédents, groupe sanguin... → dépend de : users (ProfilPatient)

medecins/       → informations professionnelles du médecin 
→ planning, disponibilité, spécialité... → dépend de : users (ProfilMedecin)

rendezvous/     → un patient prend rendez-vous avec un médecin 
→ date, heure, statut (confirmé/annulé/en attente) → dépend de : patients + medecins

consultations/  → ce qui se passe pendant le rendez-vous 
→ diagnostic, ordonnance, notes du médecin → dépend de : rendezvous + patients + medecins

notifications/  → alertes automatiques → "votre rendez-vous est confirmé" 
→ "rappel dans 24h" → dépend de : rendezvous + consultations

test 123