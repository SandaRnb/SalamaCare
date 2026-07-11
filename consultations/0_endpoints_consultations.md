GET    /api/consultations/                                       → toutes les consultations
POST   /api/consultations/creer/                                 → créer une consultation
GET    /api/consultations/1/                                     → détail consultation n°1
PUT    /api/consultations/1/                                     → modifier consultation n°1
DELETE /api/consultations/1/                                     → supprimer consultation n°1
GET    /api/consultations/patient/<int:patient_id>/              → consultations du patient n°1
GET    /api/consultations/medecin/<int:medecin_id>/              → consultations du médecin n°1
POST   /api/consultations/1/ordonnances/                         → ajouter une ordonnance
DELETE /api/consultations/<int:consultation_id>/ordonnances/<int:ordonnance_id>/        → supprimer une ordonnance