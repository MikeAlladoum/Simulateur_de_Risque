# 📊 GRAPHIQUES MATPLOTLIB & SEABORN

## ✅ INSTALLATION DES DÉPENDANCES

Les libraires matplotlib et seaborn ont été ajoutées à `requirements.txt` :

```
matplotlib>=3.8.0
seaborn>=0.13.0
```

### Installer les dépendances

```bash
cd c:\Users\HP\Documents\Simulateur_Risques\backend
pip install -r requirements.txt
```

---

## 📈 FONCTIONNALITÉS DES GRAPHIQUES

### 1. **Histogramme avec Seuils** (Graphique Principal)
```python
ChartGenerator.generate_histogram()
```

**Affiche :**
- Histogramme des pertes (barres bleues)
- Ligne Moyenne (verte)
- Ligne VaR 95% (orange pointillé)
- Ligne VaR 99% (rouge pointillé)
- Légende avec montants en FCFA
- Axes formatés (M pour millions, K pour milliers)

**Exemple :**
```python
from backend.app.simulation.chart_generator import ChartGenerator

generator = ChartGenerator()
image_base64 = generator.generate_histogram(losses, statistics)
```

---

### 2. **Box Plot**
```python
ChartGenerator.generate_box_plot()
```

**Affiche :**
- Box plot (quartiles)
- Points individuels (scatter)
- Détection des outliers
- Montants formatés en FCFA

**Utilisation :**
```python
generator = ChartGenerator()
image_base64 = generator.generate_box_plot(losses)
```

---

### 3. **Graphique de Densité (KDE)**
```python
ChartGenerator.generate_density_plot()
```

**Affiche :**
- Courbe de densité (kernel density estimation)
- Histogramme léger en background
- Estimation lisse de la distribution

**Utilisation :**
```python
generator = ChartGenerator()
image_base64 = generator.generate_density_plot(losses)
```

---

### 4. **Graphique de Comparaison**
```python
ChartGenerator.generate_comparison_chart()
```

**Affiche :**
- Graphique à barres
- Comparaison de plusieurs valeurs
- Valeurs affichées sur les barres
- Couleurs différentes

**Utilisation :**
```python
data = {
    'Moyenne': 5250000,
    'Min': 0,
    'Max': 25500000,
    'VaR 95%': 18750000,
    'VaR 99%': 22100000
}
image_base64 = generator.generate_comparison_chart(data)
```

---

## 🎨 CARACTÉRISTIQUES DES GRAPHIQUES

### Styling Seaborn
```python
sns.set_style("whitegrid")     # Style avec grille
sns.set_palette("husl")        # Palette de couleurs harmonieuse
```

### Formatage des Montants
- **Millions :** `1 000 000` → `1M`
- **Milliers :** `50 000` → `50K`
- **Devise :** Tous les montants en **FCFA**

### Qualité des Images
- **DPI :** 100 (bon compromis qualité/taille)
- **Format :** PNG (transparent background)
- **Encodage :** Base64 (transport via JSON)
- **Size :** ~50-200 KB par image

---

## 🔄 FLUX INTÉGRATION

```
Frontend (HTTP POST)
    ↓
Backend API (/api/simulate)
    ↓
MonteCarlo.simulate() [Génère losses]
    ↓
StatisticsCalculator [Calcule stats]
    ↓
ChartGenerator.generate_histogram() [Matplotlib/Seaborn]
    ↓
Image Base64 + JSON
    ↓
Frontend (Affichage dans <img>)
```

---

## 📝 EXEMPLE COMPLET

### Backend (Python)

```python
from app.simulation.monte_carlo import MonteCarlo
from app.simulation.statistics import StatisticsCalculator
from app.simulation.chart_generator import ChartGenerator

# Simulation
mc = MonteCarlo(lambda_param=5, mu_param=1000, num_simulations=10000)
losses = mc.simulate()

# Statistiques
stats_calc = StatisticsCalculator(losses)
stats = stats_calc.calculate_all()

# Graphique
generator = ChartGenerator()
chart_image = generator.generate_histogram(losses, stats.to_dict())

# Réponse JSON
response = {
    'success': True,
    'statistics': stats.to_dict(),
    'chart_image': chart_image,  # Base64 PNG
    'parameters': {...}
}
```

### Frontend (JavaScript)

```javascript
// Réception de la réponse
const response = await fetch('/api/simulate', {
    method: 'POST',
    body: JSON.stringify(params)
});

const data = await response.json();

// Affichage du graphique
if (data.chart_image) {
    const img = new Image();
    img.src = 'data:image/png;base64,' + data.chart_image;
    document.getElementById('chart-container').appendChild(img);
}
```

---

## 🛠️ PERSONNALISATION

### Changer les Couleurs

**Dans `chart_generator.py` :**

```python
def generate_histogram(self, losses, statistics, bins=50):
    # Changer les couleurs
    self.ax.hist(..., color='#YOUR_COLOR_HERE')
    self.ax.axvline(mean, color='#GREEN_HERE')
    self.ax.axvline(var_95, color='#ORANGE_HERE')
    self.ax.axvline(var_99, color='#RED_HERE')
```

### Ajuster la Taille des Graphiques

```python
# Figsize : (largeur, hauteur) en pouces
self.fig, self.ax = plt.subplots(figsize=(12, 7))  # 12" × 7"
```

### Changer la Résolution

```python
# DPI (dots per inch)
self.fig.savefig(buffer, format='png', dpi=100)  # Changer 100 ici
```

---

## ⚙️ DÉPANNAGE

### Erreur : "No module named 'matplotlib'"

```bash
pip install matplotlib>=3.8.0
```

### Erreur : "No module named 'seaborn'"

```bash
pip install seaborn>=0.13.0
```

### Graphique vide ou pixelisé

1. Vérifier le DPI (100 est standard)
2. Vérifier la figsize (12, 7) est raisonnable
3. Vérifier que les données ne sont pas vides

### Image ne s'affiche pas au frontend

1. Vérifier la réponse JSON contient `chart_image`
2. Vérifier que le base64 n'est pas vide
3. Ouvrir DevTools (F12) pour voir les erreurs

---

## 📊 COMPARAISON : Chart.js vs Matplotlib

| Aspect | Chart.js | Matplotlib |
|--------|----------|------------|
| **Lieu de génération** | Frontend (JS) | Backend (Python) |
| **Performance** | Rapide | Plus lent |
| **Interactivité** | Excellente | Statique |
| **Qualité print** | Moyenne | Excellente |
| **Contrôle** | Limité | Complet |
| **Dépendances** | CDN | pip |
| **Statistiques** | Non | Oui (Seaborn) |

**Ici on utilise Matplotlib/Seaborn côté backend pour :**
- ✅ Contrôle total des graphiques
- ✅ Style professionnel (Seaborn)
- ✅ Qualité d'impression
- ✅ Formatage avancé

---

## 🚀 PROCHAINES ÉTAPES

Pour ajouter d'autres graphiques :

```python
# Créer une nouvelle méthode
def generate_violin_plot(self, losses):
    """Graphique de distribution avec violins"""
    self.fig, self.ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=losses, ax=self.ax)
    return self._figure_to_base64()

# Ajouter un endpoint pour l'API
@api_bp.route('/visualize/violin', methods=['POST'])
def violin_chart():
    # ... implementation
```

---

## 📞 NOTES

- Les images sont générées à la volée (pas de cache)
- Chaque simulation génère une nouvelle image
- Les images sont en base64 (transmission directe via JSON)
- Compatible avec tous les navigateurs modernes

**Graphiques prêts à l'emploi !** 🎨📈
