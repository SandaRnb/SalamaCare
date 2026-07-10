GET    /api/rendezvous/                         → Lister tous les RDV
POST    /api/rendezvous/creer/                  → Créer un RDV
GET     /api/rendezvous/<rdv_id>/               → Détail d'un RDV
DELETE  /api/rendezvous/<rdv_id>/               → Supprimer un RDV
PUT     /api/rendezvous/<rdv_id>/statut/        → Modifier le statut
GET     /api/rendezvous/patient/<patient_id>/   → RDV d'un patient
GET     /api/rendezvous/medecin/<medecin_id>/   → RDV d'un médecin