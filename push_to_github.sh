#!/bin/bash
# Script pour initialiser et pousser le projet sur GitHub
# À exécuter depuis le répertoire racine du projet

# ==================== CONFIGURATION ====================
REPO_URL="https://github.com/MikeAlladoum/Simulateur_de_Risque.git"
BRANCH="main"
VERSION="v0.1"

echo "🚀 SimRisque - GitHub Push (v0.1)"
echo "=================================="

# ==================== STEP 1: Initialiser Git ====================
echo ""
echo "📦 Step 1: Initializing Git repository..."
git init
git config user.name "Mike Alladoum"
git config user.email "alladoum.michael@example.com"

# ==================== STEP 2: Ajouter tous les fichiers ====================
echo "📝 Step 2: Adding all files..."
git add .

# ==================== STEP 3: Premier commit ====================
echo "✍️  Step 3: Creating initial commit..."
git commit -m "feat: Initial commit v0.1

- Backend Flask avec API REST
- Simulation Monte Carlo (Poisson + Exponentielle)
- Calcul de statistiques (VaR, CVaR, quantiles)
- Interface frontend moderne avec thème sombre
- Visualisations Plotly interactives
- Support FCFA avec locale fr-FR
- Design responsive (mobile-first)
- CORS enabled pour cross-origin requests"

# ==================== STEP 4: Ajouter le remote GitHub ====================
echo "🔗 Step 4: Adding GitHub remote..."
git remote add origin $REPO_URL

# ==================== STEP 5: Créer et pousser la branche main ====================
echo "📤 Step 5: Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Push completed successfully!"
echo ""
echo "📊 Repository: $REPO_URL"
echo "🏷️  Version: $VERSION"
echo "📍 Branch: main"
echo ""
echo "Accédez à: https://github.com/MikeAlladoum/Simulateur_de_Risque"
