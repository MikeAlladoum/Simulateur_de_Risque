# Configuration Vercel pour le Simulateur de Risques

## Variables d'Environnement Requises

Sur Vercel, ajouter ces variables d'environnement:

### BACKEND_URL
- **Description**: URL du backend Flask (ex: https://backend-app.herokuapp.com)
- **Exemple**: `https://simulateur-backend.herokuapp.com`
- **Requise**: OUI
- **Note**: Doit être l'URL complète sans trailing slash

## Déployer le Backend

### Option 1: Render.com (Recommandé - Gratuit)
1. Aller sur [https://render.com](https://render.com)
2. Créer un nouveau Web Service
3. Sélectionner le repo GitHub
4. Configurer:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `python backend/app.py`
   - **Environment**: Python 3.11
5. Ajouter la variable d'environnement `PORT=5000`
6. Copier l'URL du service
7. Sur Vercel, ajouter `BACKEND_URL` avec cette URL

### Option 2: Railway.app
1. Aller sur [https://railway.app](https://railway.app)
2. Créer un nouveau projet
3. Connecter le repo GitHub
4. Configurer le fichier de déploiement
5. Copier l'URL du service

### Option 3: Heroku (Payant)
1. Créer une app Heroku
2. Connecter le repo GitHub
3. Déployer le backend
4. Copier l'URL

## Configuration locale (développement)

Pour tester en local:
1. Terminal 1: `python backend/app.py` (port 5000)
2. Terminal 2: `cd frontend && python -m http.server 8000` (port 8000)
3. Accéder à `http://localhost:8000`

Le frontend détectera automatiquement que c'est du développement et utilisera `localhost:5000`

## Dépannage

Si "Chargement des sinistres..." reste bloqué:
1. Vérifier que le backend est déployé
2. Vérifier la variable `BACKEND_URL` sur Vercel
3. Vérifier que le backend est accessible depuis le navigateur
4. Vérifier la console du navigateur (F12) pour les erreurs CORS
