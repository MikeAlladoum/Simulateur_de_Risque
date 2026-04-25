# Script PowerShell pour initialiser et pousser sur GitHub
# À exécuter depuis le répertoire racine du projet

param(
    [string]$RepoUrl = "https://github.com/MikeAlladoum/Simulateur_de_Risque.git",
    [string]$Version = "v0.1",
    [string]$Branch = "main"
)

Write-Host "🚀 SimRisque - GitHub Push ($Version)" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""

# ==================== STEP 1: Vérifier si Git est installé ====================
$gitExists = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitExists) {
    Write-Host "❌ Git n'est pas installé ou non accessible" -ForegroundColor Red
    Write-Host "Téléchargez Git: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Git trouvé" -ForegroundColor Green

# ==================== STEP 2: Initialiser Git ====================
Write-Host ""
Write-Host "📦 Initialisation du repo Git..." -ForegroundColor Cyan
git init
git config user.name "Mike Alladoum"
git config user.email "alladoum.michael@example.com"

# ==================== STEP 3: Ajouter tous les fichiers ====================
Write-Host ""
Write-Host "📝 Ajout de tous les fichiers..." -ForegroundColor Cyan
git add .

# ==================== STEP 4: Vérifier le status ====================
Write-Host ""
Write-Host "📊 Fichiers à commiter:" -ForegroundColor Cyan
git status --short | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }

# ==================== STEP 5: Premier commit ====================
Write-Host ""
Write-Host "✍️  Création du commit initial..." -ForegroundColor Cyan

$commitMessage = @"
feat: Initial commit $Version

- Backend Flask avec API REST
- Simulation Monte Carlo (Poisson + Exponentielle)
- Calcul de statistiques (VaR, CVaR, quantiles)
- Interface frontend moderne avec thème sombre
- Visualisations Plotly interactives
- Support FCFA avec locale fr-FR
- Design responsive (mobile-first)
- CORS enabled pour cross-origin requests
"@

git commit -m $commitMessage

# ==================== STEP 6: Ajouter le remote GitHub ====================
Write-Host ""
Write-Host "🔗 Configuration du remote GitHub..." -ForegroundColor Cyan

# Vérifier si le remote existe déjà
$remoteExists = git config --get remote.origin.url -ErrorAction SilentlyContinue
if ($remoteExists) {
    Write-Host "  Remote 'origin' existe déjà: $remoteExists" -ForegroundColor Yellow
    git remote remove origin
}

git remote add origin $RepoUrl
Write-Host "  ✅ Remote ajouté: $RepoUrl" -ForegroundColor Green

# ==================== STEP 7: Push vers GitHub ====================
Write-Host ""
Write-Host "📤 Envoi vers GitHub..." -ForegroundColor Cyan
git branch -M main
git push -u origin main --force

# ==================== Résumé ====================
Write-Host ""
Write-Host "✅ Push complété avec succès!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Repository: $RepoUrl" -ForegroundColor Yellow
Write-Host "🏷️  Version: $Version" -ForegroundColor Yellow
Write-Host "📍 Branch: $Branch" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Accédez à: https://github.com/MikeAlladoum/Simulateur_de_Risque" -ForegroundColor Cyan
Write-Host ""

# ==================== Afficher les stats ====================
Write-Host "📈 Statistiques du repo:" -ForegroundColor Cyan
$stats = @"
Branch:       $(git rev-parse --abbrev-ref HEAD)
Commits:      $(git rev-list --count HEAD)
Last commit:  $(git log -1 --format="%h - %s (%ci)")
URL:          $(git remote get-url origin)
"@
Write-Host $stats -ForegroundColor Gray
