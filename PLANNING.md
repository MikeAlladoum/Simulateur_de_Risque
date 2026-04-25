# 📅 PLANNING DÉTAILLÉ - 5 SEMAINES

---

## 🎯 VISION GÉNÉRALE

| Semaine | Phase | Objectif | Livrables |
|---------|-------|----------|-----------|
| 1 | **Analyse** | Cahier des charges + UML | CDC + Diagrammes |
| 2-4 | **Développement** | Code + tests | Application fonctionnelle |
| 5 | **Finalisation** | Soutenance | Présentation + documentation |

---

## 📌 SEMAINE 1 : ANALYSE & CONCEPTION (SPRINT 0/0bis)

### 🎓 Cahier des Charges (CDC)
- [x] Contexte et justification
- [x] Problématique
- [x] Objectifs (principal + spécifiques)
- [x] Utilisateurs cibles
- [x] Fonctionnalités (principales, secondaires, avancées)

### 📐 Cahier d'Analyse
- [ ] Diagramme de cas d'utilisation
- [ ] Diagramme de classes
- [ ] Diagramme de séquence
- [ ] Flux de données
- [ ] Architecture technique

### 📊 Répartition de l'équipe
| Membre | Tâche |
|--------|-------|
| **MIKE** | Analyse des besoins techniques (simulation, calculs) |
| **KPATCHA** | Analyse UX/UI, Wireframes |
| **GADIELLE** | Architecture globale, Diagrammes UML |

### ✅ Critères de fin
- Cahier des charges validé par l'encadrant
- Diagrammes UML complets
- Architecture décidée (Flask vs FastAPI)
- Environnement de dev configuré

---

## ⚙️ SEMAINE 2-3 : FONDATION & MOTEUR (SPRINT 1 & 2)

### SPRINT 1 : Infrastructure & Fondation

#### 🔧 MIKE - Moteur de Simulation
```
Objectif : Créer un moteur Monte Carlo fonctionnel
Durée : 3-4 jours

Tasks :
□ Mettre en place l'environnement Python
□ Implémenter classe MonteCarlo
□ Implémenter loi de Poisson
□ Implémenter loi exponentielle
□ Implémenter calculs statistiques (moyenne, std, min, max)
□ Tests unitaires

Livrables :
- simulation.py fonctionnel
- distributions.py
- statistics.py
- 10+ tests unitaires
```

#### 🎨 KPATCHA - Interface de Base
```
Objectif : Créer l'interface HTML/CSS de base
Durée : 2-3 jours

Tasks :
□ Wireframes en Figma/Pencil
□ HTML structure (formulaire)
□ CSS design responsive
□ Assets/Logo
□ Pages statiques (about, help)

Livrables :
- index.html structuré
- style.css complet
- Responsive design validé
```

#### 🚀 GADIELLE - Infrastructure
```
Objectif : Mettre en place l'environnement
Durée : 2 jours

Tasks :
□ Repository Git configuré
□ Structure des dossiers créée
□ Requirements.txt compilé
□ Documentation de base (README)
□ Script de setup

Livrables :
- Repository GitHub prêt
- README.md
- setup.sh / setup.bat
```

---

### SPRINT 2 : API & Intégration

#### 🔧 MIKE - API REST
```
Objectif : Exposer la simulation via une API
Durée : 3-4 jours

Tasks :
□ Créer application Flask
□ Endpoint POST /api/simulate
□ Validation des paramètres
□ Gestion des erreurs
□ Endpoint GET /api/health
□ Tests API

Livrables :
- app.py avec Flask
- validators.py
- API fonctionnelle testée
```

#### 🎨 KPATCHA - Formulaire + Visualisation
```
Objectif : Créer interface interactive
Durée : 3-4 jours

Tasks :
□ Formulaire interactif (HTML + JS)
□ Validation côté client (JavaScript)
□ Affichage des résultats
□ Histogramme basique (Chart.js)
□ Indicateurs statistiques
□ Responsive mobile

Livrables :
- ui.js complet
- validation.js
- index.html final
- Formulaire testé
```

#### 🚀 GADIELLE - Tests & Intégration
```
Objectif : Tester l'intégration
Durée : 3 jours

Tasks :
□ Tests unitaires backend (pytest)
□ Tests unitaires frontend (jest optionnel)
□ Tests d'intégration
□ Documentation des tests
□ CI/CD basique (GitHub Actions optionnel)

Livrables :
- Suite de tests
- Documentation des tests
- Rapports de couverture
```

---

## 📊 SEMAINE 4 : ANALYSE & VISUALISATIONS (SPRINT 3 & 4)

### SPRINT 3 : Indicateurs Avancés

#### 🔧 MIKE - Calculs Avancés
```
Objectif : Implémenter VaR, CVaR, Expected Shortfall
Durée : 2-3 jours

Tasks :
□ VaR 95%
□ VaR 99%
□ CVaR (Expected Shortfall)
□ Probabilité de dépassement
□ Analyse de sensibilité (optionnel)

Livrables :
- statistics.py amélioré
- Tests pour chaque indicateur
```

#### 🎨 KPATCHA - Graphiques Avancés
```
Objectif : Ajouter courbe de densité et comparaison
Durée : 2-3 jours

Tasks :
□ Courbe de densité (kernel density)
□ Histogramme amélioré
□ Histogramme cumulatif
□ Comparaison de scénarios
□ Légendre + annotations

Livrables :
- charts/density.js
- charts/histogram.js
- UI de comparaison
```

### SPRINT 4 : Optimisations

#### Optimisations Transversales
```
Tasks :
□ Performance optimization
□ Code cleanup
□ Refactoring
□ Documentation code
□ Amélioration UX
```

---

## 🎨 SEMAINE 5 : FINALISATION & PRÉSENTATION (SPRINT 5)

### 📝 Documentation Complète
```
Livrables requis :
□ README.md complet
□ Guide d'utilisation
□ Guide de développement
□ API documentation
□ Formules mathématiques expliquées
□ Architecture documentation
```

### 🧪 Tests Finaux
```
Tasks :
□ Tests complets (couverture > 80%)
□ Débogagement
□ Performance testing
□ Validation mathématique
□ Tests utilisateur (UX)
```

### 🎓 Préparation Soutenance
```
MIKE :
- Expliquer moteur Monte Carlo
- Montrer formules
- Démonstration simulation

KPATCHA :
- Présenter interface
- Montrer responsivité
- Expliquer UX

GADIELLE :
- Architecture du projet
- Processus de développement
- Tests et qualité
- Résultats et améliorations
```

### 📊 Présentations
```
Slides PowerPoint/Google Slides :
1. Contexte et objectifs (5 min)
2. Architecture technique (5 min)
3. Démonstration en live (10 min)
4. Résultats et indicateurs (5 min)
5. Défis et solutions (5 min)
6. Questions (10 min)

Total : 40 minutes max
```

---

## 📌 DÉPENDANCES ENTRE TÂCHES

```
SEMAINE 1 (Analyse)
    ↓
SEMAINE 2-3 (Développement)
    ├─ MIKE : Moteur simulation  ──→ API
    ├─ KPATCHA : HTML/CSS  ──→ Formulaire
    └─ GADIELLE : Infrastructure
        ↓
SEMAINE 4 (Améliorations)
    ├─ VaR, CVaR
    ├─ Graphiques avancés
    └─ Optimisations
        ↓
SEMAINE 5 (Finalisation)
    ├─ Tests finaux
    ├─ Documentation
    └─ Soutenance
```

---

## ✅ CHECKLIST PAR SEMAINE

### Semaine 1 ✓
- [ ] CDC rédigé et validé
- [ ] UML diagrammes créés
- [ ] Technos choisies
- [ ] Équipe alignée

### Semaine 2-3 ✓
- [ ] Moteur de simulation fonctionnel
- [ ] Interface HTML/CSS créée
- [ ] API REST opérationnelle
- [ ] Intégration frontend/backend
- [ ] Tests unitaires passants

### Semaine 4 ✓
- [ ] Indicateurs avancés implémentés
- [ ] Graphiques interactifs
- [ ] Comparaison de scénarios
- [ ] Tests > 80% couverture

### Semaine 5 ✓
- [ ] Documentation complète
- [ ] Tous les tests passent
- [ ] Présentations prêtes
- [ ] Démo en live fonctionnelle

---

**Bonne chance ! 🚀**
