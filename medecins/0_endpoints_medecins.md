GET    /api/medecins/                       → lister les médecins
POST   /api/medecins/inscription/           → créer un médecin
GET    /api/medecins/<int:medecin_id>/      → rechercher un médecin
PUT    /api/medecins/<int:medecin_id>/      → modifier un médecin
DELETE /api/medecins/<int:medecin_id>/      → supprimer un médecin