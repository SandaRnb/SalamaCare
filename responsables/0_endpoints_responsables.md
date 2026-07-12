GET    /api/responsables/                          → lister les responsables
GET    /api/responsables/<int:responsable_id>/       → rechercher un responsable
PUT    /api/responsables/<int:responsable_id>/       → modifier un responsable
DELETE /api/responsables/<int:responsable_id>/        → supprimer un responsable

# Gestion patient
GET    /api/responsables/patients/recherche/          → rechercher un patient existant
POST   /api/responsables/patients/creer/              → créer un dossier patient

# Attribution médecin
POST   /api/responsables/patients/<int:patient_id>/attribuer/    → attribuer un patient à un médecin

# Rendez-vous
GET    /api/responsables/rendezvous/                  → lister les rendez-vous (agenda)
POST   /api/responsables/rendezvous/creer/             → créer un rendez-vous
PUT    /api/responsables/rendezvous/<int:rdv_id>/reporter/   → reporter un rendez-vous
DELETE /api/responsables/rendezvous/<int:rdv_id>/annuler/    → annuler un rendez-vous

# Consultation
POST   /api/responsables/consultations/<int:consultation_id>/assigner/   → assigner une consultation

# Notification
POST   /api/responsables/notifications/envoyer/        → envoyer une notification à un médecin

# Suivi
GET    /api/responsables/patients/statut/              → voir le statut des patients