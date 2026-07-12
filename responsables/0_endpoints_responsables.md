GET    /api/responsables/patients/recherche/?q=<username>   → rechercher un patient existant (par username)
POST   /api/users/register/patient/                          → créer un dossier patient (User + ProfilPatient)
POST   /api/rendezvous/creer/                                → créer un rendez-vous / attribuer un patient à un médecin
PUT    /api/rendezvous/<int:rdv_id>/statut/                  → annuler un rendez-vous (statut=annule) ou reporter (date_heure)
GET    /api/rendezvous/                                      → lister l'agenda (filtré selon le rôle connecté)
POST   /api/notifications/envoyer/                           → envoyer une notification à un médecin
GET    /api/responsables/patients/statut/                    → voir le statut de tous les patients (déduit du dernier RDV)
