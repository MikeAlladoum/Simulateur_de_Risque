# 📑 INDEX DU PROJET

---

## 📚 DOCUMENTATION PRINCIPALE

| Document | Description | Rôle |
|----------|-------------|------|
| [README.md](README.md) | Guide d'utilisation complet | Tous |
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | Vue d'ensemble du projet | Chef de projet |
| [PLANNING.md](PLANNING.md) | Planning par sprints détaillé | Chef de projet |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture technique du système | Architecte/Tous |
| [AMELIORATIONS.md](AMELIORATIONS.md) | Améliorations futures et points d'extension | Tous |

---

## 🔧 BACKEND (Python/Flask)

### Configuration et Démarrage
- **[config.py](backend/config.py)** - Configuration globale
- **[run.py](backend/run.py)** - Point d'entrée serveur
- **[requirements.txt](backend/requirements.txt)** - Dépendances Python

### Code Métier
- **[app/__init__.py](backend/app/__init__.py)** - Initialisation Flask
- **[app/models.py](backend/app/models.py)** - Modèles de données
- **[app/api.py](backend/app/api.py)** - Endpoints API REST

### Moteur de Simulation
- **[app/simulation/monte_carlo.py](backend/app/simulation/monte_carlo.py)** - Moteur principal
- **[app/simulation/distributions.py](backend/app/simulation/distributions.py)** - Lois Poisson/Exponentielle
- **[app/simulation/statistics.py](backend/app/simulation/statistics.py)** - Calculs statistiques (VaR, CVaR)
- **[app/simulation/validators.py](backend/app/simulation/validators.py)** - Validation des paramètres

### Utilitaires
- **[app/utils/helpers.py](backend/app/utils/helpers.py)** - Fonctions utilitaires
- **[app/utils/converters.py](backend/app/utils/converters.py)** - Conversion de formats

### Tests Unitaires
- **[app/tests/test_monte_carlo.py](backend/app/tests/test_monte_carlo.py)** - Tests du moteur MC
- **[app/tests/test_distributions.py](backend/app/tests/test_distributions.py)** - Tests des lois
- **[app/tests/test_statistics.py](backend/app/tests/test_statistics.py)** - Tests des statistiques

### Documentation Backend
- **[docs/API_SPEC.md](backend/docs/API_SPEC.md)** - Spécification API complète
- **[docs/FORMULES.md](backend/docs/FORMULES.md)** - Formules mathématiques expliquées

---

## 🌐 FRONTEND (HTML/CSS/JavaScript)

### Pages HTML
- **[index.html](frontend/index.html)** - Page principale (formulaire + résultats)

### Styles
- **[styles.css](frontend/styles.css)** - Design système CSS complet

### Configuration
- **[config.js](frontend/config.js)** - Configuration globale frontend

### JavaScript Core
- **[js/main.js](frontend/js/main.js)** - Point d'entrée + initialisation
- **[js/api.js](frontend/js/api.js)** - Client API REST
- **[js/validation.js](frontend/js/validation.js)** - Validation des formulaires
- **[js/ui.js](frontend/js/ui.js)** - Gestion interface utilisateur

### Graphiques
- **[js/charts/chart-config.js](frontend/js/charts/chart-config.js)** - Configuration Chart.js
- **[js/charts/histogram.js](frontend/js/charts/histogram.js)** - Gestion histogramme

### Utilitaires
- **[js/utils/formatters.js](frontend/js/utils/formatters.js)** - Formatage nombres/devises
- **[js/utils/helpers.js](frontend/js/utils/helpers.js)** - Fonctions JavaScript utilitaires

---

## 📊 DONNÉES

- **[data/example_data.json](data/example_data.json)** - Données d'exemple et scénarios
- **[.env.example](.env.example)** - Configuration environnement (à adapter)

---

## 🛠️ SCRIPTS

- **[scripts/setup.sh](scripts/setup.sh)** - Installation Linux/macOS
- **[scripts/setup.bat](scripts/setup.bat)** - Installation Windows

---

## 🎯 FLUX TYPIQUE

### 1. Arborescence Complète

```
Simulateur_Risques/
│
├── 📄 README.md                 ← COMMENCEZ ICI
├── 📄 PROJECT_OVERVIEW.md
├── 📄 PLANNING.md
├── 📄 ARCHITECTURE.md
├── 📄 AMELIORATIONS.md
├── 📄 INDEX.md                  ← (Ce fichier)
├── 📄 .env.example
├── 📄 .gitignore
│
├── 🔧 backend/
│   ├── 📄 config.py
│   ├── 📄 run.py                ← Démarrer : python run.py
│   ├── 📄 requirements.txt       ← pip install -r requirements.txt
│   │
│   ├── 📁 app/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 models.py
│   │   ├── 📄 api.py
│   │   │
│   │   ├── 📁 simulation/       ← MOTEUR MONTE CARLO
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 monte_carlo.py
│   │   │   ├── 📄 distributions.py
│   │   │   ├── 📄 statistics.py
│   │   │   └── 📄 validators.py
│   │   │
│   │   ├── 📁 utils/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 helpers.py
│   │   │   └── 📄 converters.py
│   │   │
│   │   └── 📁 tests/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 test_monte_carlo.py
│   │       ├── 📄 test_distributions.py
│   │       └── 📄 test_statistics.py
│   │
│   └── 📁 docs/
│       ├── 📄 API_SPEC.md
│       └── 📄 FORMULES.md
│
├── 🌐 frontend/
│   ├── 📄 index.html            ← Ouvrir dans navigateur
│   ├── 📄 styles.css
│   ├── 📄 config.js
│   │
│   └── 📁 js/
│       ├── 📄 main.js
│       ├── 📄 api.js
│       ├── 📄 validation.js
│       ├── 📄 ui.js
│       │
│       ├── 📁 charts/
│       │   ├── 📄 chart-config.js
│       │   └── 📄 histogram.js
│       │
│       └── 📁 utils/
│           ├── 📄 formatters.js
│           └── 📄 helpers.js
│
├── 📊 data/
│   ├── 📄 example_data.json
│   └── 📄 historical_data.csv   (future)
│
└── 🛠️ scripts/
    ├── 📄 setup.sh
    └── 📄 setup.bat
```

---

## 🚀 GUIDE DE DÉMARRAGE RAPIDE

### Pour les Développeurs

**1. Clone et installation**
```bash
cd Simulateur_Risques
./scripts/setup.sh  # ou setup.bat sur Windows
```

**2. Démarrer le backend**
```bash
cd backend
python run.py
# Output: 🚀 Démarrage du serveur...
#         📍 URL : http://127.0.0.1:5000
```

**3. Ouvrir le frontend**
Double-cliquez sur `frontend/index.html` ou lancez un serveur local

**4. Tester**
```bash
cd backend
pytest app/tests/ -v
```

---

## 👥 RÉPARTITION PAR RÔLE

### MIKE - Backend
- Fichiers à modifier : `backend/app/simulation/`, `backend/app/api.py`
- Objectifs : Implémenter/améliorer le moteur, ajouter des lois, optimiser
- Tests : `backend/app/tests/`

### KPATCHA - Frontend
- Fichiers à modifier : `frontend/index.html`, `frontend/styles.css`, `frontend/js/`
- Objectifs : Améliorer UI/UX, ajouter graphiques, animations
- Tests : Tests manuels dans le navigateur

### GADIELLE - QA/Integration
- Fichiers à vérifier : Tous
- Objectifs : Tests, documentation, déploiement
- Tests : Tous les fichiers de test

---

## 📋 CHECKLIST DÉVELOPPEMENT

### Semaine 1 : Fondation
- [ ] Environnement Python configuré
- [ ] Dépendances installées
- [ ] Moteur MC fonctionnel
- [ ] Tests Poisson + Exponentielle passants
- [ ] Interface HTML basique

### Semaine 2 : Intégration
- [ ] API Flask opérationnelle
- [ ] Endpoint /api/simulate fonctionnel
- [ ] Frontend formulaire prêt
- [ ] Intégration frontend/backend
- [ ] Statistiques affichées

### Semaine 3 : Finalisation
- [ ] Graphiques interactifs
- [ ] VaR + CVaR implémentés
- [ ] Tests > 80% couverture
- [ ] Documentation complète
- [ ] Prêt pour soutenance

---

## 🔗 RESSOURCES RAPIDES

### Exécution
- Backend : `python backend/run.py`
- Tests : `pytest backend/app/tests/ -v`
- Frontend : Ouvrir `frontend/index.html`

### Documentation
- API : `backend/docs/API_SPEC.md`
- Maths : `backend/docs/FORMULES.md`
- Architecture : `ARCHITECTURE.md`

### Débugage
- Logs backend : Console lors du `python run.py`
- Logs frontend : Console du navigateur (F12)
- API health : `http://localhost:5000/api/health`

---

## ❓ FAQ Rapide

**Q: Erreur "Module not found" ?**
A: Lancez `pip install -r requirements.txt`

**Q: API non accessible ?**
A: Vérifiez que `python run.py` tourne sur le port 5000

**Q: Simulation très lente ?**
A: Réduisez `num_simulations` dans le formulaire

**Q: Comment ajouter une loi ?**
A: Voir `AMELIORATIONS.md` section "Points de Personnalisation"

---

**Bonne chance ! 🚀**

*Projet : Simulateur de Risques Financiers*  
*Établissement : UCAO-UUT*  
*Année : 2025-2026*  
*Groupe : 8*
