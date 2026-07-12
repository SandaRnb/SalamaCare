GET    /api/patients/                       → lister les médecins
POST   /api/patients/inscription/           → créer un médecin
GET    /api/patients/<int:patient_id>/      → rechercher un médecin
PUT    /api/patients/<int:patient_id>/      → modifier un médecin
DELETE /api/patients/<int:patient_id>/      → supprimer un médecin