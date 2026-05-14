# SQLite Database Documentation

## Vue d'ensemble

L'application utilise maintenant **SQLite** comme base de données locale pour persister les données :
- **Fichier**: `backend/simulateur.db`
- **ORM**: SQLAlchemy (Flask-SQLAlchemy)
- **Auto-init**: Créé automatiquement au premier démarrage

## Modèles de Données

### 1. User (Utilisateurs)
```sql
- id (Integer, Primary Key)
- username (String, Unique)
- email (String, Unique)
- role (String) - 'user', 'admin', etc.
- created_at (DateTime)
- updated_at (DateTime)
```

### 2. Simulation (Résultats de simulations)
```sql
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key → User)
- profile_id (Integer, Foreign Key → Profile, Optional)
- num_simulations (Integer) - Nombre de runs
- sinistres_config (JSON) - Configuration des sinistres
- statistics (JSON) - Statistiques globales
- statistics_by_type (JSON) - Stats par type de sinistre
- histogram (JSON) - Données histogramme
- name (String, Optional)
- description (Text, Optional)
- created_at (DateTime)
- updated_at (DateTime)
```

### 3. Profile (Configurations sauvegardées)
```sql
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key → User)
- name (String) - Nom du profil
- description (Text, Optional)
- domain (String, Optional) - Domaine d'activité
- default_num_simulations (Integer) - Nombre de simulations par défaut
- sinistres_config (JSON) - Configuration des sinistres
- is_default (Boolean) - Profil par défaut
- created_at (DateTime)
- updated_at (DateTime)
```

## Endpoints API

### Simulations

#### Sauvegarder une simulation
```bash
POST /api/simulations/save
Content-Type: application/json

{
  "user_id": 1,
  "num_simulations": 10000,
  "sinistres_config": {...},
  "statistics": {...},
  "statistics_by_type": {...},
  "histogram": {...},
  "name": "Simulation Q2 2024",
  "description": "Analyse risques secteur assurance"
}

Response: 
{
  "success": true,
  "simulation_id": 1,
  "message": "Simulation sauvegardée"
}
```

#### Récupérer une simulation
```bash
GET /api/simulations/1

Response:
{
  "id": 1,
  "user_id": 1,
  "num_simulations": 10000,
  "sinistres_config": {...},
  "statistics": {...},
  ...
}
```

#### Lister les simulations d'un utilisateur
```bash
GET /api/simulations?user_id=1

Response:
{
  "success": true,
  "count": 5,
  "simulations": [...]
}
```

#### Supprimer une simulation
```bash
DELETE /api/simulations/1

Response:
{
  "success": true,
  "message": "Simulation supprimée"
}
```

### Profils

#### Créer un profil
```bash
POST /api/profiles
Content-Type: application/json

{
  "user_id": 1,
  "name": "Profil Prudent",
  "description": "Configuration pour stratégie prudente",
  "domain": "Assurance",
  "default_num_simulations": 5000,
  "sinistres_config": {
    "consultation": {"lambda": 2.0, "cout_moyen": 5000},
    "hospitalisation": {"lambda": 0.3, "cout_moyen": 250000}
  },
  "is_default": true
}

Response:
{
  "success": true,
  "profile_id": 1,
  "message": "Profil créé"
}
```

#### Récupérer un profil
```bash
GET /api/profiles/1

Response:
{
  "id": 1,
  "user_id": 1,
  "name": "Profil Prudent",
  ...
}
```

#### Lister les profils d'un utilisateur
```bash
GET /api/profiles?user_id=1

Response:
{
  "success": true,
  "count": 3,
  "profiles": [...]
}
```

#### Supprimer un profil
```bash
DELETE /api/profiles/1

Response:
{
  "success": true,
  "message": "Profil supprimé"
}
```

## Utilisation avec Frontend

### Flux actuel (Stateless)
1. Frontend lance simulation → Backend calcule résultats
2. Résultats affichés dans le navigateur
3. ❌ Données perdues au rechargement

### Flux avec BD (Persistant)
1. Frontend lance simulation → Backend calcule résultats
2. ✅ Backend sauvegarde dans SQLite
3. Résultats affichés + sauvegardés
4. ✅ Données retrouvées après rechargement
5. ✅ Historique accessible

### Exemple: Sauvegarde après simulation
```javascript
// Dans frontend/js/app.js (à implémenter)
async function saveSimulationToDB(results) {
  const response = await fetch('http://localhost:5000/api/simulations/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: 1,
      num_simulations: results.num_simulations,
      sinistres_config: results.sinistres_config,
      statistics: results.statistics,
      statistics_by_type: results.statistics_by_type,
      histogram: results.histogram,
      name: `Simulation ${new Date().toLocaleDateString()}`,
      description: 'Simulation Monte Carlo'
    })
  });
  
  const data = await response.json();
  console.log('Simulation ID:', data.simulation_id);
  return data;
}
```

## Configuration Production

### Base de données PostgreSQL
Pour la production, utiliser PostgreSQL à la place de SQLite :

```python
# backend/app.py
import os

# Développement
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///simulateur.db')

# Production (Heroku, Railway, etc)
# DATABASE_URL='postgresql://user:password@host:port/dbname'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

### Migration (si nécessaire)
```bash
# Installer Flask-Migrate
pip install Flask-Migrate

# Initialiser migrations
flask db init

# Créer migration
flask db migrate -m "Initial migration"

# Appliquer migration
flask db upgrade
```

## Sauvegarde et Restauration

### Sauvegarder la BD
```bash
# SQLite - simple copie du fichier
cp backend/simulateur.db backups/simulateur_backup.db
```

### Restaurer la BD
```bash
# Arrêter l'app
# Remplacer le fichier
cp backups/simulateur_backup.db backend/simulateur.db
# Relancer l'app
```

## Nettoyage de la BD

### Réinitialiser la base de données
```python
# Dans le shell Python
from backend.app import app, db
from backend.models import User, Simulation, Profile

with app.app_context():
    db.drop_all()  # ⚠️ Supprime toutes les tables
    db.create_all()  # Recrée les tables vides
```

## Déploiement

### Vercel + PostgreSQL (Recommandé)
1. Créer base PostgreSQL sur Render.com ou Neon
2. Ajouter variable d'env Vercel: `DATABASE_URL='postgresql://...'`
3. Backend sur Render détecte `DATABASE_URL` automatiquement

### Vercel + SQLite (Limité)
⚠️ SQLite stocké sur disque éphémère Vercel → données perdues après redéploiement
→ Recommandé uniquement pour développement local

## Voir aussi

- [Backend README](./README.md)
- [Configuration Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
