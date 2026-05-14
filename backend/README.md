# 🎯 Simulateur de Risques Financiers - Guide Démarrage

## 📋 Prérequis

- Python 3.8+
- Node.js (optionnel, pour servir le frontend)

## 🚀 Installation & Démarrage

### 1️⃣ **Backend Flask**

```bash
cd backend

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur
python run.py
```

Le serveur démarre sur `http://localhost:5000`

**Endpoints disponibles:**
- `GET /api/health` - Vérification du statut
- `POST /api/simulate` - Lancer une simulation
- `GET /api/profiles` - Lister les profils
- `GET /api/info` - Information API

### 2️⃣ **Frontend**

#### Option A: Serveur Python simple

```bash
cd frontend
python -m http.server 8000
```

Accès sur `http://localhost:8000`

#### Option B: Node.js (si installé)

```bash
cd frontend
npx http-server -p 8000
```

#### Option C: Ouvrir directement

```bash
cd frontend
start index.html
```

## 📡 Configuration API

Modifier `frontend/config.js`:

```javascript
const CONFIG = {
    API: {
        BASE_URL: 'http://localhost:5000/api',
        ...
    }
};
```

## 🧪 Tester l'API

### Avec cURL:

```bash
# Health check
curl http://localhost:5000/api/health

# Simulation
curl -X POST http://localhost:5000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "lambda": 5,
    "mu": 1000,
    "num_simulations": 10000,
    "distribution": "normal"
  }'
```

### Avec Postman:

1. Créer une requête POST
2. URL: `http://localhost:5000/api/simulate`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "lambda": 5,
  "mu": 1000,
  "num_simulations": 10000,
  "distribution": "normal"
}
```

## 🎨 Architecture

```
Simulateur_de_Risque/
├── frontend/
│   ├── index.html
│   ├── main.css
│   ├── config.js
│   └── js/
│       ├── app.js
│       ├── api.js
│       ├── auth.js
│       └── ...
├── backend/
│   ├── app.py          # API Flask principale
│   ├── run.py          # Script de démarrage
│   ├── requirements.txt # Dépendances Python
│   └── __init__.py
└── README.md
```

## 📊 Simulations Disponibles

**Distributions supportées:**
- `normal` - Distribution normale
- `lognormal` - Distribution log-normale
- `uniform` - Distribution uniforme

**Paramètres:**
- `lambda` - Paramètre de forme (0.01 - 1000)
- `mu` - Paramètre de moyenne (0.01 - 1000000)
- `num_simulations` - Nombre de simulations (1 - 100000)

## 🐛 Dépannage

### Port déjà utilisé

```bash
# Trouver le processus
netstat -ano | findstr :5000

# Tuer le processus (Windows)
taskkill /PID <PID> /F
```

### Module non trouvé

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### CORS errors

Vérifier que `Flask-CORS` est installé et activé dans `app.py`

## 📚 Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Monte Carlo Method](https://en.wikipedia.org/wiki/Monte_Carlo_method)

## 🔒 Notes de Sécurité

**En développement local:**
- ✅ CORS activé (accepte toutes les origines)
- ✅ Debug mode activé
- ✅ Pas d'authentification

**En production:**
- ❌ Désactiver debug mode
- ❌ Configurer CORS pour domaines spécifiques
- ❌ Ajouter authentification JWT
- ❌ Utiliser HTTPS

## 📝 Licence

MIT - © MikeAlladoum

---

**Besoin d'aide?**
Consultez les fichiers de configuration ou la documentation technique PDF.
