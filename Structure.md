salamacare_api/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── users/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models.py       → User + ProfilMedecin + ProfilPatient + ProfilResponsable
│   ├── serializers.py  → Token + Register (3 rôles)
│   ├── permissions.py  → IsResponsable + IsMedecin + IsPatient + ...
│   ├── views.py        → Login + Register (3 rôles)
│   ├── urls.py         → /login/ /register/... /token/refresh/
│   └── admin.py
│
├── patients/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models.py       → DossierPatient
│   ├── serializers.py  → DossierPatientSerializer
│   ├── services.py     → logique métier (créer dossier, rechercher...)
│   ├── views.py        → CRUD patients
│   ├── urls.py         → /api/patients/
│   └── admin.py
│
├── medecins/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models.py       → Disponibilite
│   ├── serializers.py  → DisponibiliteSerializer
│   ├── services.py     → logique métier (planning, disponibilités...)
│   ├── views.py        → CRUD médecins
│   ├── urls.py         → /api/medecins/
│   └── admin.py
│
├── rendezvous/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models.py       → RendezVous
│   ├── serializers.py  → RendezVousSerializer
│   ├── services.py     → logique métier (créer rdv, vérifier dispo...)
│   ├── views.py        → CRUD rendez-vous
│   ├── urls.py         → /api/rendezvous/
│   └── admin.py
│
├── consultations/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models.py       → Consultation
│   ├── serializers.py  → ConsultationSerializer
│   ├── services.py     → logique métier (créer consultation, ordonnance...)
│   ├── views.py        → CRUD consultations
│   ├── urls.py         → /api/consultations/
│   └── admin.py
│
├── notifications/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models.py       → Notification
│   ├── serializers.py  → NotificationSerializer
│   ├── services.py     → logique métier (envoyer, marquer lu...)
│   ├── views.py        → liste + marquer comme lu
│   ├── urls.py         → /api/notifications/
│   └── admin.py
│
├── env/
├── manage.py
├── requirements.txt
└── .env


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