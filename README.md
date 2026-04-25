# 📊 Simulateur de Risques Financiers - Monte Carlo

Application web professionnelle pour simuler et analyser les risques financiers en utilisant la méthode Monte Carlo avec visualisations dynamiques et interactives.

## ✨ Fonctionnalités

✅ **Simulation Monte Carlo** - Génération aléatoire de sinistres selon une loi de Poisson  
✅ **Distributions flexibles** - Support de multiples lois (Poisson, Exponentielle, Lognormale)  
✅ **Statistiques complètes** - Moyenne, min, max, écart-type, médiane, VaR (95% & 99%)  
✅ **Graphiques interactifs** - Histogrammes, box plots, graphiques de densité avec Plotly  
✅ **Design responsive** - Interface moderne compatible mobile/tablet/desktop  
✅ **Validation en temps réel** - Feedback utilisateur immédiat  
✅ **Architecture professionnelle** - REST API, tests unitaires, documentation complète  

## 📋 Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Un navigateur moderne (Chrome, Firefox, Edge, Safari)

## 🚀 Installation et Démarrage Rapide

### Étape 1 : Installer les dépendances Python

```bash
cd backend
pip install -r requirements.txt
```

### Étape 2 : Lancer le serveur backend

```bash
python run.py
```

Le serveur Flask démarrera sur `http://127.0.0.1:5000`

### Étape 3 : Ouvrir l'application frontend

**Option 1 :** Double-cliquez sur `frontend/index-new.html`

**Option 2 :** Utilisez un serveur local
```bash
cd frontend
python -m http.server 8000
```
Puis accédez à `http://localhost:8000`

## 💡 Comment utiliser

1. **Entrez les paramètres de simulation :**
   - **λ (Lambda)** - Fréquence moyenne des sinistres (0.01 à 1000)
   - **μ (Mu)** - Coût moyen d'un sinistre (0.01 à 1 000 000)
   - **N** - Nombre de simulations (100 à 1 000 000)

2. **Cliquez sur "Lancer la simulation"**

3. **Explorez les résultats :**
   - Statistiques clés affichées dans des cartes
   - Graphiques interactifs (zoom, pan, hover tooltips)
   - Visualisations en temps réel avec Plotly

## 📁 Structure du Projet

```
Seminaire_MIDA/
├── backend/
│   ├── app/
│   │   ├── simulation/           # Moteur Monte Carlo
│   │   │   ├── monte_carlo.py   # Simulation vectorisée
│   │   │   ├── statistics.py    # Calculs statistiques
│   │   │   ├── distributions.py # Distributions de probabilité
│   │   │   ├── validators.py    # Validation des entrées
│   │   │   └── chart_generator.py # Génération graphiques Plotly
│   │   ├── utils/               # Utilitaires
│   │   ├── tests/               # Tests unitaires
│   │   ├── api.py               # Routes Flask REST
│   │   ├── models.py            # Structures de données
│   │   └── __init__.py          # Initialisation
│   ├── config.py                # Configuration
│   ├── run.py                   # Point d'entrée
│   ├── requirements.txt         # Dépendances Python
│   └── app.py                   # Application Flask
│
├── frontend/
│   ├── index-new.html           # Page principale (moderne)
│   ├── styles-modern.css        # Design system complet
│   ├── config.js                # Configuration frontend
│   ├── js/
│   │   ├── api.js               # Client API REST
│   │   ├── main-modern.js       # Logique principale
│   │   ├── ui-modern.js         # Gestion de l'interface
│   │   ├── validation.js        # Validation formulaire
│   │   ├── charts/              # Configuration graphiques
│   │   └── utils/               # Utilitaires JS
│   └── assets/                  # Images et ressources
│
├── Documentation/
│   ├── README.md                # Ce fichier
│   ├── ARCHITECTURE.md          # Architecture technique
│   ├── PROJECT_OVERVIEW.md      # Vue d'ensemble
│   ├── DESIGN_MODERN_GUIDE.md   # Guide du design
│   └── DEMARRAGE_RAPIDE.md      # Démarrage rapide
│
└── .env.example                 # Variables d'environnement
```

## 🏗️ Architecture Technique

### Architecture en Couches

```
Frontend (HTML/CSS/JavaScript)
    ↓ HTTP/JSON (API REST)
API REST (Flask)
    ↓
Moteur de Simulation (NumPy)
    ↓
Générateur de Graphiques (Plotly)
    ↓
Résultats JSON avec charts interactifs
```

### Stack Technologique

**Backend :**
- Python 3.8+
- Flask 2.3+ (REST API)
- NumPy 1.25+ (calculs vectorisés)
- Plotly 5.0+ (visualisations interactives)
- Flask-CORS (gestion CORS)
- pytest (tests)

**Frontend :**
- HTML5 + CSS3 (responsive design)
- Vanilla JavaScript (pas de framework)
- Plotly.js (graphiques interactifs)

## 📊 Statistiques et Indicateurs

### Statistiques Descriptives
- **Moyenne** : Perte moyenne simulée
- **Médiane** : Perte au point médian
- **Min/Max** : Pertes extrêmes (minimum et maximum)
- **Écart-type** : Mesure de variabilité

### Indicateurs de Risque
- **VaR 95%** : Perte maximale probable (95% confiance)
- **VaR 99%** : Perte maximale probable (99% confiance)
- **Cas zéro-perte** : Nombre de simulations sans sinistres

## 🧪 Tests

Lancer la suite de tests :

```bash
cd backend
pytest app/tests/ -v
```

Résultats :
- Tests de distributions
- Tests de simulation Monte Carlo
- Tests de calculs statistiques
- Couverture : 90%+

## 📚 Documentation des Endpoints API

### GET /api/health

Vérifier l'état du serveur

**Réponse :**
```json
{
    "status": "healthy",
    "version": "0.1.0"
}
```

### GET /api/info

Informations sur l'API

**Réponse :**
```json
{
    "name": "Financial Risk Simulator API",
    "version": "0.1.0",
    "endpoints": [...],
    "constraints": {
        "lambda": [0.01, 1000],
        "mu": [0.01, 1000000],
        "num_simulations": [100, 1000000]
    }
}
```

### POST /api/simulate

Lancer une simulation

**Requête :**
```json
{
    "lambda": 5,
    "mu": 1000,
    "num_simulations": 10000
}
```

**Réponse (succès) :**
```json
{
    "success": true,
    "statistics": {
        "mean": 5045.23,
        "median": 4890.45,
        "min": 0,
        "max": 23450.67,
        "std": 3421.89,
        "var_95": 12345.67,
        "var_99": 18901.23,
        "num_zero_loss": 125
    },
    "histogram": {
        "bins": [...],
        "frequencies": [...]
    },
    "parameters": {
        "lambda": 5,
        "mu": 1000,
        "num_simulations": 10000
    },
    "chart_json": "{"data":[...],...}"  # Plotly JSON interactif
}
```

## 🔧 Configuration

### Backend (.env)

```
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
HOST=127.0.0.1
```

### Frontend (config.js)

```javascript
CONFIG = {
    API_URL: 'http://127.0.0.1:5000/api',
    CURRENCY: {
        CODE: 'FCFA',
        SYMBOL: 'FCFA',
        LOCALE: 'fr-FR'
    },
    CONSTRAINTS: {
        lambda: { min: 0.01, max: 1000 },
        mu: { min: 0.01, max: 1000000 },
        num_simulations: { min: 100, max: 1000000 }
    }
}
```

## 🐛 Dépannage

### Erreur : "Impossible de se connecter à l'API"
- Vérifiez que le serveur Flask est lancé : `python run.py`
- Vérifiez que le port 5000 est libre : `netstat -ano | findstr :5000`
- Vérifiez les logs du serveur Flask

### Erreur CORS
- Flask-CORS est activé par défaut dans `app/__init__.py`
- Vérifiez que l'en-tête `Access-Control-Allow-Origin` est présent

### Graphiques ne s'affichent pas
- Vérifiez que Plotly est installé : `pip list | grep plotly`
- Ouvrez la console JavaScript (F12) et vérifiez les erreurs
- Vérifiez que `chart_json` est présent dans la réponse API

### Simulation très lente
- Réduisez `num_simulations` (commencez par 10 000)
- Les calculs vectorisés NumPy sont normalement très rapides

## 👥 Équipe du Projet

- **MIKE** - Backend (simulation + API)
- **KPATCHA** - Frontend (interface + UX)
- **GADIELLE** - Intégration + tests + validation

**Encadrant :** M. WOAMEY  
**Séminaire :** MIDA (Machine Learning & Data Analysis)  
**Établissement :** UCAO-UUT (Université Catholique d'Afrique de l'Ouest)  
**Année Académique :** 2025-2026  
**Lieu :** Togo

## 📝 Licence

Projet académique - UCAO-UUT Togo

---

**Besoin d'aide ?**
- Consultez la documentation complète dans les fichiers `.md`
- Vérifiez les tests unitaires pour des exemples d'utilisation
- Ouvrez une issue ou contactez l'équipe

**Dernier mise à jour :** Avril 2026  
**Version :** 1.0.0
