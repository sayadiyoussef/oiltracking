# Oiltracker — Installation locale (dev)

## Prérequis
- Docker & Docker Compose
- Git

## Étapes
1. Clonez le dépôt puis placez-vous dans `infrastructure/`.
2. Lancez:
   ```bash
   docker compose up --build
   ```
3. API: http://localhost:8000/docs — Front: http://localhost:3000

## Données de test
- Chargez `data/seed.sql` dans la base (ou utilisez SQLite en changeant `DATABASE_URL`).
- CSV dans `data/` pour marché/grades.

## Environnements hébergement
- **GitHub** pour code + Actions CI/CD
- **Vercel** pour le front Next.js
- **AWS (RDS + EC2 + S3 + SES)** pour back et services

## Notes
Ce package est un socle minimal viable pour démonstration.
Il correspond au cahier des charges et schéma ERD fournis, dont modules marché, fixings, alertes et chat (squelettes). 
Mise en prod conseillée via images Docker, secrets GitHub et infra as-code.
