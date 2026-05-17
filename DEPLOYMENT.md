# 🚀 Guide de Déploiement - Simulateur de Risques

## Architecture

```
Navigateur
    ↓
Vercel (Frontend static)
    ↓
Handler.py (API Gateway)
    ↓
Render.com (Backend Flask)
    ↓
SQLite Database
```

---

## ✅ ÉTAPE 1: Déployer le Backend sur Render.com

### 1.1 Créer un compte Render
- Aller sur https://render.com
- S'inscrire avec GitHub

### 1.2 Créer un Web Service
1. Cliquer sur **"New Web Service"**
2. Sélectionner ton repo GitHub: `Simulateur_de_Risque`
3. Remplir:
   - **Name**: `simulateur-backend`
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `python backend/app.py`
   - **Plan**: Free

### 1.3 Configurer les variables d'environnement
Ajouter sur Render:
```
PYTHON_VERSION = 3.13
PORT = 5000
FLASK_ENV = production
DATABASE_URL = sqlite:///simulateur.db
```

### 1.4 Déployer
- Cliquer **"Create Web Service"**
- Attendre 3-5 minutes
- **COPIER L'URL** (ex: `https://simulateur-backend-xxx.onrender.com`)

---

## ✅ ÉTAPE 2: Configurer Vercel avec l'URL du Backend

### 2.1 Accéder à Vercel
- Aller sur https://vercel.com
- Se connecter avec GitHub

### 2.2 Importer le projet
1. Cliquer **"Add New"** → **"Project"**
2. Sélectionner le repo `Simulateur_de_Risque`
3. Cliquer **"Import"**

### 2.3 Ajouter la variable d'environnement
1. Aller dans **"Settings"** → **"Environment Variables"**
2. Ajouter:
   ```
   BACKEND_URL = https://simulateur-backend-xxx.onrender.com
   ```
   (Remplacer `xxx` par ton vrai ID Render)

3. Cliquer **"Add"**

### 2.4 Déployer
1. Revenir au dashboard
2. Cliquer **"Redeploy"** ou attendre auto-deployment
3. **COPIER L'URL Vercel** (ex: `https://simulateur-de-risque.vercel.app`)

---

## ✅ ÉTAPE 3: Tester

### Test 1: Frontend accessible
```
Navigateur → https://simulateur-de-risque.vercel.app
```
Doit afficher la page de login ✅

### Test 2: Backend accessible
```
Navigateur → https://simulateur-backend-xxx.onrender.com/api/health
```
Doit afficher:
```json
{"status": "ok"}
```

### Test 3: API Gateway fonctionnel
```
Navigateur → https://simulateur-de-risque.vercel.app/api/health
```
Doit afficher le status du backend ✅

### Test 4: Simulation complète
1. Se connecter: `demo` / `demo123`
2. Lancer une simulation
3. Vérifier les résultats

---

## 🔧 URLs à utiliser

| Composant | URL Locale | URL Production |
|-----------|-----------|-----------------|
| Frontend | http://localhost:8000 | https://simulateur-de-risque.vercel.app |
| Backend | http://localhost:5000 | https://simulateur-backend-xxx.onrender.com |
| API | http://localhost:5000/api | https://simulateur-de-risque.vercel.app/api |

---

## ❌ Dépannage

### Le frontend ne se charge pas
- Vérifier que Vercel a bien l'URL du backend en variable d'environnement
- Redéployer: https://vercel.com → Dashboard → Project → Redeploy

### L'API retourne "Not found"
- Vérifier que le backend Render est actif
- Vérifier l'URL dans Vercel → Settings → Environment Variables

### La simulation retourne une erreur
- Vérifier la console du navigateur (F12)
- Vérifier les logs Render: https://render.com → Dashboard → Services → Logs

---

## 📝 Variables d'environnement finales

### Sur Render.com (Backend)
```
PYTHON_VERSION = 3.13
PORT = 5000
FLASK_ENV = production
DATABASE_URL = sqlite:///simulateur.db
```

### Sur Vercel (Frontend)
```
BACKEND_URL = https://simulateur-backend-xxx.onrender.com
```

---

## ✨ Résumé pour toi

1. **Render.com**: Crée un Web Service → Copie l'URL
2. **Vercel**: Importe le projet → Ajoute BACKEND_URL → Redéploie
3. **Test**: Accède à Vercel et teste la simulation

C'est tout! 🎉
