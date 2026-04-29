# 🚀 COMMENCER EN 5 MINUTES

---

## ✅ Prérequis

- ✅ Python 3.8+ ( vérifier : `python --version` )
- ✅ pip ( vérifier : `pip --version` )
- ✅ Navigateur web moderne

---

## 🚀 DÉMARRAGE EN 3 ÉTAPES

### Étape 1️⃣ : Installer les dépendances

```bash
cd backend
pip install -r requirements.txt
```

**⏱️ Temps : ~1 minute**

✅ Vous verrez : `Successfully installed Flask, numpy, ...`

---

### Étape 2️⃣ : Lancer le serveur backend

```bash
python run.py
```

**⏱️ Temps : immédiat**

✅ Vous verrez :
```
╔═══════════════════════════════════════════════════════╗
║   Simulateur de Risques Financiers - Backend         ║
║   Version 0.1.0                                       
╚═══════════════════════════════════════════════════════╝

🚀 Démarrage du serveur...
📍 URL : http://127.0.0.1:5000
🔧 Mode : development
🐛 Debug : True
```

⚠️ **Laissez ce terminal OUVERT**

---

### Étape 3️⃣ : Ouvrir l'application

**Option A : Clic simple**
- Double-cliquez sur `frontend/index.html`
- ✅ L'application s'ouvre dans votre navigateur

**Option B : Serveur local (recommandé)**
```bash
# Dans un nouveau terminal
cd frontend
python -m http.server 8000
```
Puis allez à `http://localhost:8000`

---

## ✨ C'est tout ! Vous êtes prêt !

La page s'affiche ? Parfait ! 🎉

**Maintenant, testez :**

1. **Entrez les paramètres par défaut** (λ=5, μ=1000, N=10000)
2. **Cliquez "Lancer la simulation"**
3. **Regardez les résultats s'afficher** ✨

---

## 📋 Que fait chaque partie ?

| Composant | Rôle | Fichier |
|-----------|------|---------|
| **Backend** | Effectue la simulation Monte Carlo | `python run.py` |
| **API** | Expose les résultats en JSON | `backend/app/api.py` |
| **Frontend** | Affiche l'interface utilisateur | `frontend/index.html` |
| **Graphique** | Visualise les pertes | `frontend/js/charts/` |

---

## 🧪 Tester les fonctionnalités

### Test 1 : Simulation basique
```
λ = 5
μ = 1000
N = 10000
→ Lancer → Voir les résultats
```

### Test 2 : Simulation rapide
```
λ = 5
μ = 1000
N = 1000  (au lieu de 10000)
→ Plus rapide !
```

### Test 3 : Simulation précise
```
λ = 5
μ = 1000
N = 100000  (attention : plus long!)
→ Plus précis
```

---

## 🔍 Déboguer (si problème)

### Problème : API non accessible

```
⚠️ Erreur : "Impossible de se connecter à l'API"
```

**Solution :**
```bash
# Vérifier que le serveur tourne
curl http://localhost:5000/api/health

# Si erreur "Connection refused" :
# → Retourner au terminal et lancez : python run.py
```

### Problème : Port 5000 occupé

```
⚠️ Erreur : "Address already in use"
```

**Solution :**
```bash
# Sur Windows :
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Sur Linux/Mac :
lsof -i :5000
kill -9 <PID>

# Puis relancez : python run.py
```

### Problème : Module manquant

```
⚠️ Erreur : "ModuleNotFoundError: No module named 'flask'"
```

**Solution :**
```bash
pip install -r backend/requirements.txt
```

---

## 📖 Prochaines étapes

### Lire la documentation
1. [README.md](README.md) - Guide complet
2. [ARCHITECTURE.md](ARCHITECTURE.md) - Comment ça marche
3. [INDEX.md](INDEX.md) - Structure du projet

### Explorer le code
- **Backend** : Ouvrez `backend/app/simulation/monte_carlo.py`
- **Frontend** : Ouvrez `frontend/js/main.js`

### Lancer les tests
```bash
cd backend
pytest app/tests/ -v
```

---

## 💡 Conseils

✅ **Gardez les deux terminaux ouverts :**
- Terminal 1 : Backend (python run.py)
- Terminal 2 : Travail / Tests

✅ **Utilisez F12 dans le navigateur** pour voir les logs (onglet Console)

✅ **Changez les paramètres** et observez comment les résultats changent

✅ **Consultez le Code** pour comprendre comment ça fonctionne

---

## 🎓 Votre Mission

### Semaine 1
- ✅ Installer et lancer l'app
- ✅ Comprendre le flux frontend→API→Backend
- ✅ Lire la documentation

### Semaine 2
- ✅ Modifier le code (ajouter une loi, améliorer UI)
- ✅ Voir vos changements en temps réel
- ✅ Tester vos modifications

### Semaine 3
- ✅ Améliorer et optimiser
- ✅ Préparer la présentation
- ✅ 🎉 Soutenance !

---

## 🆘 Aide Supplémentaire

### Consulter la documentation
- [API_SPEC.md](backend/docs/API_SPEC.md) - Endpoints API
- [FORMULES.md](backend/docs/FORMULES.md) - Formules mathématiques
- [PLANNING.md](PLANNING.md) - Planning des développements

### Contacter l'équipe
- MIKE - Backend : `backend/app/simulation/`
- KPATCHA - Frontend : `frontend/js/`
- GADIELLE - Tests : `backend/app/tests/`

---

## ✨ Résumé

| Étape | Commande | Temps |
|-------|----------|-------|
| 1. Installation | `pip install -r backend/requirements.txt` | 1 min |
| 2. Backend | `python backend/run.py` | 0 min |
| 3. Frontend | Double-clic `frontend/index.html` | 0 min |
| **TOTAL** | | **~1 min** ⚡ |

---

## 🎉 Bravo !

Vous avez une application de simulation Monte Carlo fonctionnelle et prête à être améliorée !

**À vous de jouer ! 🚀**

---

*Besoin d'aide ?* Consultez [INDEX.md](INDEX.md) pour la structure complète
