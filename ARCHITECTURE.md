# 🏗️ ARCHITECTURE TECHNIQUE

---

## 1️⃣ ARCHITECTURE GÉNÉRALE

```
┌─────────────────────────────────────────────────────────────┐
│                    WEB BROWSER (Frontend)                   │
│                   HTML/CSS/JavaScript                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                                                        │  │
│  │     Formulaire → Validation → Appel API → Affichage │  │
│  │                                                        │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP (POST/GET)
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                  API REST (Flask/FastAPI)                   │
│                                                             │
│  /api/simulate  (POST)                                     │
│  /api/health    (GET)                                      │
│  /api/scenarios (GET, POST, DELETE)                        │
└──────────────────┬──────────────────────────────────────────┘
                   │ Python
                   ↓
┌─────────────────────────────────────────────────────────────┐
│              MOTEUR DE SIMULATION (Backend)                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │          Classe MonteCarlo                          │  │
│  │  - simulate()                                       │  │
│  │  - get_statistics()                                 │  │
│  │  - get_probabilities()                              │  │
│  └─────────────────────────────────────────────────────┘  │
│                        ↓                                    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │        Distributions Statistiques                   │  │
│  │  - Poisson(λ) → Nombre de sinistres              │  │
│  │  - Exponential(μ) → Coûts individuels             │  │
│  └─────────────────────────────────────────────────────┘  │
│                        ↓                                    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │          Calculs Statistiques                       │  │
│  │  - Moyenne, Min, Max, Écart-type                   │  │
│  │  - VaR 95%, VaR 99%                                │  │
│  │  - CVaR, Expected Shortfall                        │  │
│  │  - Probabilités                                     │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2️⃣ STRUCTURE DES FICHIERS

### Backend (Python)

```
backend/
│
├── config.py
│   └─ Configuration (debug, port, etc.)
│
├── run.py
│   └─ Point d'entrée principal
│
├── requirements.txt
│   └─ Dépendances Python
│
└── app/
    │
    ├── __init__.py
    │   └─ Initialisation Flask
    │
    ├── models.py
    │   └─ Classes de données (SimulationRequest, SimulationResult)
    │
    ├── api.py
    │   └─ Routes Flask et endpoints API
    │
    ├── simulation/
    │   ├── __init__.py
    │   │
    │   ├── monte_carlo.py
    │   │   └─ Classe MonteCarlo (moteur principal)
    │   │
    │   ├── distributions.py
    │   │   ├─ poisson_generator(λ)
    │   │   └─ exponential_generator(μ)
    │   │
    │   ├── statistics.py
    │   │   ├─ calculate_stats()
    │   │   ├─ calculate_var()
    │   │   ├─ calculate_cvar()
    │   │   └─ calculate_probability()
    │   │
    │   └── validators.py
    │       └─ Validation des paramètres
    │
    ├── utils/
    │   ├── __init__.py
    │   ├── helpers.py
    │   │   └─ Fonctions utilitaires
    │   │
    │   └── converters.py
    │       └─ Conversion formats JSON ↔ Python
    │
    └── tests/
        ├── __init__.py
        ├── test_monte_carlo.py
        ├── test_distributions.py
        ├── test_statistics.py
        └── test_api.py
```

### Frontend (Web)

```
frontend/
│
├── index.html
│   └─ Page principale
│
├── styles.css
│   └─ Styles CSS (responsif, mobile-first)
│
├── config.js
│   └─ Configuration (URL API, thèmes)
│
└── js/
    │
    ├── main.js
    │   └─ Point d'entrée (init, event listeners)
    │
    ├── api.js
    │   └─ Client API REST
    │       ├─ POST /api/simulate
    │       ├─ GET /api/health
    │       └─ GET /api/scenarios
    │
    ├── ui.js
    │   └─ Gestion interface utilisateur
    │       ├─ displayResults()
    │       ├─ showLoading()
    │       └─ showError()
    │
    ├── validation.js
    │   └─ Validation formulaires (côté client)
    │       ├─ validateLambda()
    │       ├─ validateMu()
    │       └─ validateNumSimulations()
    │
    ├── charts/
    │   ├── histogram.js
    │   │   └─ Graphique histogramme (Chart.js)
    │   │
    │   ├── density.js
    │   │   └─ Courbe de densité (D3.js)
    │   │
    │   └── chart-config.js
    │       └─ Configuration Chart.js
    │
    └── utils/
        ├── formatters.js
        │   └─ formatNumber(), formatCurrency()
        │
        └── helpers.js
            └─ Fonctions utilitaires JavaScript
```

---

## 3️⃣ FLUX DE DONNÉES

### Scénario 1 : Simulation

```
User Input (Frontend)
    ↓
[λ, μ, N]
    ↓
Validation (Frontend)
    ↓ ✅ Valide
POST /api/simulate
{
  "lambda": 5,
  "mu": 1000,
  "num_simulations": 10000
}
    ↓
Backend - app.py (API)
    ↓
Validation (Backend)
    ↓ ✅ Valide
MonteCarlo.simulate()
    ├─ distributions.poisson_generator(λ) → N
    ├─ distributions.exponential_generator(μ) → X_i
    └─ Calcul L = Σ X_i
    ↓
statistics.calculate_stats(L)
    ├─ mean, std, min, max
    ├─ VaR 95%, VaR 99%
    ├─ CVaR
    └─ Probabilités
    ↓
JSON Response
{
  "statistics": {...},
  "histogram": {...},
  "success": true
}
    ↓
Frontend - script.js
    ↓
ui.displayResults()
    ├─ Afficher statistiques
    ├─ Afficher histogramme
    └─ Afficher indicateurs risque
    ↓
User Sees Results
```

---

## 4️⃣ TECHNOLOGIES & JUSTIFICATIONS

| Élément | Technologie | Raison |
|---------|-----------|--------|
| **Backend** | Python 3.8+ | Calculs scientifiques, NumPy, ecosystem riche |
| **Framework API** | Flask | Léger, simple, parfait pour MVP, facilement extensible |
| **Calculs numériques** | NumPy | Vectorisé, rapide, standard industrie |
| **Frontend** | HTML5/CSS3/JS | Web standard, aucune dépendance |
| **Graphiques** | Chart.js | Interactif, facile d'utilisation |
| **Tests backend** | pytest | Framework standard Python |
| **Versioning** | Git + GitHub | Collaboration d'équipe |

---

## 5️⃣ DESIGN PATTERNS

### Pattern MVC (léger)

```
Model      (backend/app/models.py)  → Classes de données
View       (frontend/index.html)     → Interface utilisateur
Controller (backend/app/api.py)      → Endpoints API
```

### Pattern Separation of Concerns

```
Simulation    (backend/app/simulation/)   → Logique métier pure
API           (backend/app/api.py)        → Exposition HTTP
UI            (frontend/js/)              → Présentation
```

### Pattern Factory

```
Créer différentes distributions :
- PoissonDistribution
- ExponentialDistribution
- (future) LogNormalDistribution
```

---

## 6️⃣ SCALABILITÉ & AMÉLIORATIONS

### Court terme (3 semaines)
- ✅ Simulation Monte Carlo basique
- ✅ VaR, CVaR
- ✅ Interface simple

### Moyen terme (optionnel)
- 📊 Données historiques (import CSV)
- 🔄 Comparaison de scénarios
- 📈 Graphiques avancés (D3.js)
- 💾 Sauvegarde résultats

### Long terme (future)
- 🗄️ Base de données (PostgreSQL)
- 🔐 Authentification utilisateur
- 📱 Application mobile
- ☁️ Déploiement cloud (Heroku, AWS)
- 🤖 ML pour prédictions

---

## 7️⃣ SÉCURITÉ

```
☑️ Validation stricte des entrées
☑️ Gestion d'erreurs robuste
☑️ CORS activé (contrôlé)
☑️ Rate limiting (optionnel)
☑️ Pas de données sensibles en frontend
☑️ Variables d'environnement pour config
```

---

## 8️⃣ PERFORMANCE

```
Optimisations à prévoir :
☑️ NumPy vectorisé (vs boucles Python)
☑️ Cache des résultats (optionnel)
☑️ Frontend : lazy loading, compression CSS/JS
☑️ API : response compression (gzip)
```

---

## ✅ CHECKLIST D'IMPLÉMENTATION

- [ ] Structure des dossiers créée
- [ ] Flask configuré
- [ ] Classe MonteCarlo prête
- [ ] API endpoints fonctionnels
- [ ] Frontend HTML/CSS
- [ ] JavaScript API client
- [ ] Tests unitaires
- [ ] Intégration frontend/backend
- [ ] Graphiques interactifs
- [ ] Documentation complète

**Bon développement ! 🚀**
