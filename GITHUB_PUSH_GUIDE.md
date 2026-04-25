# 🚀 Guide de Push sur GitHub - v0.1

## 📋 Prérequis

1. **Git installé** - https://git-scm.com/download/win
2. **Accès GitHub** - Compte configuré localement avec SSH ou Token
3. **Repository créé** - https://github.com/MikeAlladoum/Simulateur_de_Risque

## 🔑 Authentification GitHub

### Option 1: SSH (Recommandé)
```bash
# Générer une clé SSH
ssh-keygen -t ed25519 -C "your-email@example.com"

# Ajouter à l'agent SSH
ssh-add ~/.ssh/id_ed25519

# Copier la clé publique à GitHub
# Paramètres > SSH and GPG keys > New SSH key
```

### Option 2: Personal Access Token (PAT)
```bash
# Générer un token sur GitHub
# Settings > Developer settings > Personal access tokens

# Utiliser lors du prompt:
# Username: votre-username
# Password: votre-token-personnel
```

### Option 3: HTTPS avec credentials
```bash
# Windows: Git Credential Manager (inclus avec Git)
# Lors du premier push, entrer vos identifiants GitHub
```

## 📤 Exécution du Push

### Méthode 1: Script PowerShell (RECOMMANDÉ POUR WINDOWS)

```powershell
# Ouvrir PowerShell dans le répertoire du projet
cd C:\Users\HP\Documents\Seminaire_MIDA

# Exécuter le script
.\push_to_github.ps1
```

Le script va automatiquement:
1. ✅ Initialiser le repo Git
2. ✅ Ajouter tous les fichiers
3. ✅ Créer un commit initial avec message professionnel
4. ✅ Configurer le remote GitHub
5. ✅ Pousser vers la branche main

### Méthode 2: Script Bash (Pour Unix/Linux/Mac)

```bash
# Ouvrir terminal dans le répertoire du projet
cd /path/to/Seminaire_MIDA

# Exécuter le script
bash push_to_github.sh
```

### Méthode 3: Commandes manuelles (Git CLI)

```bash
# 1. Initialiser
cd C:\Users\HP\Documents\Seminaire_MIDA
git init
git config user.name "Mike Alladoum"
git config user.email "your-email@example.com"

# 2. Ajouter tous les fichiers
git add .

# 3. Vérifier les fichiers ajoutés
git status

# 4. Premier commit
git commit -m "feat: Initial commit v0.1

- Backend Flask avec API REST
- Simulation Monte Carlo (Poisson + Exponentielle)
- Calcul de statistiques (VaR, CVaR, quantiles)
- Interface frontend moderne avec thème sombre
- Visualisations Plotly interactives
- Support FCFA avec locale fr-FR
- Design responsive (mobile-first)
- CORS enabled pour cross-origin requests"

# 5. Ajouter le remote
git remote add origin https://github.com/MikeAlladoum/Simulateur_de_Risque.git

# 6. Renommer la branche et pousser
git branch -M main
git push -u origin main
```

## ✅ Vérification

Après le push, vérifiez:

1. **GitHub Repository**
   - Allez sur https://github.com/MikeAlladoum/Simulateur_de_Risque
   - Vérifiez que les fichiers sont présents

2. **Structure visible**
   ```
   Simulateur_de_Risque/
   ├── backend/
   │   ├── app/
   │   ├── run.py
   │   └── requirements.txt
   ├── frontend/
   │   ├── index.html
   │   ├── main.css
   │   └── js/
   ├── .gitignore
   ├── README.md
   └── push_to_github.ps1
   ```

3. **Commit visible**
   - Cliquez sur "Commits"
   - Vérifiez le commit initial avec tag v0.1

## 🏷️ Créer une Release (Optionnel)

Pour créer une version officielle v0.1:

```bash
# Créer un tag
git tag -a v0.1 -m "Version 0.1 - Initial Release"

# Pousser le tag
git push origin v0.1
```

Puis sur GitHub:
1. Allez à "Releases"
2. Cliquez "Create a new release"
3. Sélectionnez le tag `v0.1`
4. Ajoutez une description

## 🔄 Prochains commits

Après le premier push, vous pouvez faire des commits normaux:

```bash
# Modifier des fichiers
# ...

# Stage les modifications
git add .

# Commit
git commit -m "feat: Description de la modification"

# Push
git push origin main
```

## ⚠️ Troubleshooting

### Erreur: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/MikeAlladoum/Simulateur_de_Risque.git
```

### Erreur: "Permission denied (publickey)"
- Configurez SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Erreur: "fatal: 'origin' does not appear to be a 'git' repository"
```bash
git remote -v  # Vérifiez les remotes
git remote add origin <URL_CORRECTE>
```

### Erreur: "Updates were rejected because the tip of your current branch is behind"
```bash
git pull origin main
git push origin main
```

## 📚 Ressources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Help](https://docs.github.com)
- [Conventional Commits](https://www.conventionalcommits.org)

---

**Prêt? Exécutez: `.\push_to_github.ps1`** 🚀
