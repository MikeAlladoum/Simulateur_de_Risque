# 📊 SIMULATEUR DE RISQUES FINANCIERS
## Vue d'ensemble du projet

---

## 🎯 VISION DU PROJET

**Objectif Principal :** Créer une application web capable de simuler des scénarios de risques financiers en utilisant la méthode Monte Carlo, afin de fournir des indicateurs de risque pour aider à la prise de décision.

**Public cible :**
- Étudiants en mathématiques, statistique, actuariat
- Enseignants
- Analystes de risque
- Toute personne intéressée par la gestion des risques

---

## 📈 CONTEXTE ACADÉMIQUE

| Élément | Détail |
|---------|--------|
| **Établissement** | UCAO-UUT (Université Catholique de l'Afrique de l'Ouest - Unité Universitaire du Togo) |
| **Séminaire** | MIDA (MI = Mathématiques & Informatique, DA = Développement d'Applications) |
| **Groupe** | Groupe 8 |
| **Encadrant** | M. WOAMEY |
| **Durée** | 5 semaines (3 de développement intensif) |
| **Année académique** | 2025-2026 |

---

## 👥 ÉQUIPE DE DÉVELOPPEMENT

| Rôle | Responsable | Domaine |
|------|-------------|---------|
| **Backend** | MIKE | Simulation + API REST |
| **Frontend** | KPATCHA | Interface utilisateur + UX |
| **Intégration & Tests** | GADIELLE | Tests + validation + déploiement |

---

## 🔧 TECHNOLOGIES

| Couche | Technologie | Justification |
|--------|-----------|---------------|
| **Backend** | Python 3.8+ | Calculs scientifiques, NumPy |
| **API** | Flask / FastAPI | Légère, rapide, idéale pour MVP |
| **Calculs** | NumPy | Optimisé pour opérations vectorisées |
| **Frontend** | HTML5/CSS3/JavaScript | Web standard |
| **Graphiques** | Chart.js / D3.js | Visualisations interactives |
| **Versioning** | Git | Collaboration d'équipe |

---

## 🎓 CONCEPTS MATHÉMATIQUES CLÉS

### 1. Loi de Poisson
Distribution discrète du nombre de sinistres (événements aléatoires)
$$N \sim \text{Poisson}(\lambda)$$
- **λ** = fréquence moyenne des sinistres

### 2. Loi Exponentielle
Distribution continue des coûts individuels des sinistres
$$X_i \sim \text{Exp}(\mu)$$
- **μ** = coût moyen d'un sinistre

### 3. Perte Totale
$$L = \sum_{i=1}^{N} X_i$$

### 4. Value at Risk (VaR)
Perte maximale probable avec un niveau de confiance (95%, 99%)
$$\text{VaR}_{\alpha} = \text{quantile}(L, \alpha)$$

### 5. Expected Shortfall (CVaR)
Perte moyenne en cas de dépassement du VaR
$$\text{CVaR}_{\alpha} = \mathbb{E}[L | L \geq \text{VaR}_{\alpha}]$$

---

## ✨ FONCTIONNALITÉS

### Phase 1 : Simulation de Base (Semaine 1)
- ✅ Saisie de paramètres (λ, μ, N)
- ✅ Génération aléatoire (Poisson + Exponentielle)
- ✅ Calcul des pertes totales
- ✅ Statistiques basiques (moyenne, min, max)

### Phase 2 : Interface + Indicateurs (Semaine 2)
- ✅ Formulaire HTML/CSS
- ✅ API REST
- ✅ Intégration frontend/backend
- ✅ Indicateurs avancés (VaR 95%, VaR 99%, CVaR)
- ✅ Histogramme interactif

### Phase 3 : Visualisations + Extras (Semaine 3)
- ✅ Courbe de densité
- ✅ Comparaison de scénarios
- ✅ Données historiques (optionnel)
- ✅ Export résultats
- ✅ Tests complets

---

## 🏗️ STRUCTURE GÉNÉRALE

```
Simulateur_Risques/
├── backend/          # Python + Flask + NumPy
│   ├── app/         # Code métier
│   │   ├── simulation/      # Moteur Monte Carlo
│   │   └── utils/          # Utilitaires
│   └── tests/       # Tests unitaires
│
├── frontend/         # HTML/CSS/JavaScript
│   ├── js/          # Logique
│   ├── css/         # Styles
│   └── pages/       # Pages HTML
│
└── data/            # Données d'exemple
```

---

## 📅 PLANNING PAR SPRINTS

### Semaine 1 : Fondation
- **MIKE** : Moteur de simulation (Poisson, Exponentielle)
- **KPATCHA** : Wireframes + HTML/CSS de base
- **GADIELLE** : Architecture du projet + Git

### Semaine 2 : Intégration
- **MIKE** : API Flask + validation
- **KPATCHA** : Formulaire + affichage résultats
- **GADIELLE** : Tests unitaires + intégration

### Semaine 3 : Finalisation
- **MIKE** : Optimisations + données historiques
- **KPATCHA** : Graphiques + animations
- **GADIELLE** : Tests E2E + documentation + préparation soutenance

---

## ✅ CRITÈRES DE SUCCÈS

- [x] Simulation correcte et fiable (résultats validés mathématiquement)
- [x] Interface intuitive et responsive
- [x] API robuste avec validation d'entrées
- [x] Indicateurs de risque corrects (VaR, CVaR, etc.)
- [x] Code bien structuré et documenté
- [x] Tests > 80% de couverture
- [x] Prêt pour la soutenance

---

## 📚 DOCUMENTATION

Voir les fichiers :
- `README.md` : Guide d'utilisation
- `PLANNING.md` : Planning détaillé
- `ARCHITECTURE.md` : Architecture technique
- `backend/docs/API_SPEC.md` : Spécification API
- `backend/docs/FORMULES.md` : Formules mathématiques

---

**Bon courage pour ce projet ! 🚀**
