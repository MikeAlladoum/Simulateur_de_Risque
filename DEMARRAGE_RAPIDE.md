# Configuration rapide du projet

## 🚀 Démarrage en 3 étapes

### 1️⃣ Installer les dépendances
```bash
cd backend
pip install -r requirements.txt
```

### 2️⃣ Lancer le serveur
```bash
python app.py
```

### 3️⃣ Ouvrir le navigateur
Double-cliquez sur `frontend/index.html` ou allez à `http://localhost:8000`

---

## ✅ Vérification

- [ ] Python 3.8+ installé (`python --version`)
- [ ] Pip fonctionne (`pip --version`)
- [ ] Dépendances installées (`pip list | grep Flask`)
- [ ] Serveur démarre sans erreur
- [ ] Frontend se charge dans le navigateur
- [ ] Simulation fonctionne

---

## 📚 Notes de développement

### Pour MIKE (Backend)
Fichiers importants : `backend/app.py`, `backend/simulation.py`
- Ajouter de nouvelles lois statistiques dans `simulation.py`
- Ajouter des endpoints dans `app.py`

### Pour KPATCHA (Frontend)
Fichiers importants : `frontend/index.html`, `frontend/style.css`, `frontend/script.js`
- Améliorer l'interface dans `style.css`
- Ajouter de nouveaux graphiques dans `script.js`

### Pour GADIELLE (Tests & Intégration)
- Tester chaque fonctionnalité
- Vérifier l'intégration frontend/backend
- Documenter les bugs trouvés

---

**Bonne chance ! 🎓**
