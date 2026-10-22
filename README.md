# IncidentFlow — projet pratique DevOps Logwire

Petite API REST de gestion d'incidents en Python/FastAPI. Données stockées **en mémoire uniquement**, perdues au redémarrage. Ceci est un laboratoire, pas une application de production.

## Prérequis
- Python 3.12 et Docker Desktop (avec Compose)
- Git

## Local
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
ruff check .
python -m pytest -q
uvicorn app.main:app --reload
```
Ouvrir http://localhost:8000/docs

## Docker
```bash
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
docker compose logs -f api
docker compose down
```

## API
```bash
curl -i http://localhost:8000/health
curl -i -X POST http://localhost:8000/incidents -H 'Content-Type: application/json' -d '{"title":"API inaccessible","severity":"high"}'
curl http://localhost:8000/incidents
curl -X PATCH http://localhost:8000/incidents/1/resolve
```

## CI
Créer un dépôt GitHub, y pousser ce projet, puis regarder l'onglet Actions. Le workflow exécute lint, tests et construction de l'image sans déployer en production.

## Limitations
- Aucun stockage persistant, authentification, multi-réplicas, alerting ou déploiement distant.
- Versionnement des dépendances par plages pour un laboratoire ; en production, utiliser des versions verrouillées et des scans de sécurité.
- Le conteneur s'exécute sous un utilisateur non-root ; port exposé uniquement sur localhost côté machine hôte.
