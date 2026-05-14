# Guide de Build et Déploiement - Simulateur de Risque

## Prérequis

- Python 3.11+
- pip (gestionnaire de paquets Python)
- Navigateur web moderne

## Installation des Dépendances

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
Le frontend n'a pas de dépendances à installer. Les bibliothèques sont chargées via CDN.

## Lancement du Projet

### Option 1 : Lancement Rapide (Développement)

#### Terminal 1 - Backend Flask
```bash
cd backend
python app.py
```
Le serveur démarre sur `http://127.0.0.1:5000`

#### Terminal 2 - Frontend HTTP
```bash
cd frontend
python -m http.server 8000
```
Le frontend est accessible sur `http://127.0.0.1:8000`

### Option 2 : Depuis la Racine du Projet

#### Terminal 1 - Backend
```bash
python backend/app.py
```

#### Terminal 2 - Frontend
```bash
cd frontend && python -m http.server 8000
```

## Vérification du Statut

### Backend (API)
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/health
```

### Frontend
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000
```

## Accès à l'Application

1. Ouvrez le navigateur: `http://127.0.0.1:8000`
2. Vous serez automatiquement redirigé vers la page de connexion
3. Authentifiez-vous avec les identifiants (non affichés pour des raisons de sécurité)
4. Accédez au tableau de bord de simulation

## Structure du Projet

```
Seminaire_MIDA/
├── backend/
│   ├── app.py                 # Application Flask principale
│   ├── simulation.py           # Moteur Monte Carlo
│   ├── config.py              # Configuration et rôles utilisateurs
│   └── requirements.txt        # Dépendances Python
├── frontend/
│   ├── index.html             # Dashboard principal
│   ├── login.html             # Page d'authentification
│   ├── main.css               # Styles globaux
│   ├── config.js              # Configuration frontend
│   └── js/
│       ├── auth.js            # Gestion authentification JWT
│       ├── app.js             # Logique application
│       ├── sinistres.js       # Gestion des sinistres
│       └── ...
├── generer_cahier_analyse.py  # Générateur PDF
└── BUILD.md                   # Ce fichier

```

## Configuration

### Comptes Utilisateurs
Les comptes sont configurés dans `backend/config.py`. Chaque utilisateur a un rôle:
- `demo`: Utilisateur standard
- `admin`: Administrateur avec accès complet
- `user1`: Utilisateur standard

### Authentification
- Système JWT (JSON Web Token)
- Tokens valides 24 heures
- Tokens stockés en localStorage (côté client)

## Commandes Utiles

### Générer le Cahier d'Analyse PDF
```bash
python generer_cahier_analyse.py
```

### Vérifier la Santé du Backend
```bash
curl http://127.0.0.1:5000/api/health
# ou en PowerShell
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/health
```

### Tester l'Authentification
```powershell
$body = @{username="demo"; password="demo123"} | ConvertTo-Json
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/auth/login -Method POST -Body $body -ContentType "application/json"
```

## Arrêter les Serveurs

### Terminal Backend
Appuyez sur `Ctrl + C`

### Terminal Frontend
Appuyez sur `Ctrl + C`

## Dépannage

### Le backend ne démarre pas
```bash
# Vérifier que les dépendances sont installées
pip install -r backend/requirements.txt
```

### Le frontend ne charge pas
```bash
# Vérifier le répertoire courant
cd frontend
python -m http.server 8000
```

### Erreur de connexion au serveur
Vérifiez que:
1. Le backend Flask est lancé sur le port 5000
2. Le frontend est lancé sur le port 8000
3. Pas de pare-feu bloquant ces ports

## Production

Pour un déploiement en production:
1. Installer un serveur WSGI (Gunicorn)
2. Configurer une vraie base de données
3. Utiliser des variables d'environnement pour les secrets
4. Mettre en place HTTPS
5. Configurer CORS correctement
