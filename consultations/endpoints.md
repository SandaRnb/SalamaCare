GET    /api/consultations/                          → liste consultations
POST   /api/consultations/                          → créer consultation
GET    /api/consultations/{id}/                     → détail consultation
PUT    /api/consultations/{id}/                     → modifier consultation
GET    /api/consultations/patient/{patient_id}/     → consultations d'un patient
GET    /api/consultations/{id}/ordonnances/         → ordonnances d'une consultation
POST   /api/consultations/{id}/ordonnances/         → ajouter ordonnance
DELETE /api/consultations/ordonnances/{id}/         → supprimer ordonnance