"""
Chart Generator

Generates interactive Plotly visualizations for simulation results.
"""

import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class InteractiveChartGenerator:
    """Generate interactive charts using Plotly."""
    
    def generate_histogram(self, losses: np.ndarray, statistics: Dict, bins: int = 50) -> str:
        """
        Generate histogram HTML.
        
        Args:
            losses (np.ndarray): Simulated losses array
            statistics (Dict): Statistics dictionary
            bins (int): Number of bins for histogram
        
        Returns:
            str: HTML representation of the histogram
        """
        
        # Create histogram
        hist, bin_edges = np.histogram(losses, bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Create figure
        fig = go.Figure()
        
        # Add histogram trace
        fig.add_trace(go.Bar(
            x=bin_centers.tolist(),
            y=hist.tolist(),
            name='Distribution des Pertes',
            marker=dict(
                color='rgba(99, 102, 241, 0.7)',
                line=dict(color='rgba(99, 102, 241, 1)', width=1)
            ),
            hovertemplate='<b>Perte: %{x:.2f}</b><br>Fréquence: %{y}<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Distribution des Pertes',
                'font': {'size': 18, 'color': '#374151'}
            },
            xaxis_title='Pertes (FCFA)',
            yaxis_title='Fréquence',
            hovermode='closest',
            paper_bgcolor='#F9FAFB',
            plot_bgcolor='#FFFFFF',
            margin=dict(l=60, r=40, t=60, b=60),
            showlegend=False
        )
        
        # Convert to HTML
        return pio.to_html(fig, include_plotlyjs='cdn', div_id='histogram')
    
    def generate_summary_chart(self, statistics: Dict) -> str:
        """
        Generate summary metrics chart.
        
        Args:
            statistics (Dict): Statistics dictionary
        
        Returns:
            str: HTML representation of the summary chart
        """
        
        metrics = ['Mean', 'Median', 'Min', 'Max', 'Std Dev']
        values = [
            statistics.get('mean', 0),
            statistics.get('median', 0),
            statistics.get('min', 0),
            statistics.get('max', 0),
            statistics.get('std', 0)
        ]
        
        # Create figure
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=metrics,
            y=values,
            name='Statistics',
            marker=dict(
                color=['#6366F1', '#8B5CF6', '#EC4899', '#F59E0B', '#10B981'],
            ),
            hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title='Résumé des Statistiques',
            xaxis_title='Métrique',
            yaxis_title='Valeur (FCFA)',
            paper_bgcolor='#F9FAFB',
            plot_bgcolor='#FFFFFF',
            margin=dict(l=60, r=40, t=60, b=60),
            showlegend=False
        )
        
        return pio.to_html(fig, include_plotlyjs='cdn', div_id='summary-chart')

"""
Interactive Chart Generator - Génération des graphiques dynamiques avec Plotly

Crée des graphiques interactifs pour visualiser les résultats de la simulation
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np


class InteractiveChartGenerator:
    """
    Génère les graphiques interactifs avec Plotly
    """
    
    def __init__(self):
        """Initialise le générateur de graphiques"""
        self.fig = None
    
    def generate_histogram(self, losses, statistics, bins=50):
        """
        Génère l'histogramme dynamique des pertes
        
        Args:
            losses: Array des pertes totales
            statistics: Dict contenant mean, var_95, var_99
            bins: Nombre de bins pour l'histogramme
        
        Returns:
            str: HTML du graphique Plotly
        """
        # Calculer les bins
        hist_counts, bin_edges = np.histogram(losses, bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Créer la figure
        self.fig = go.Figure()
        
        # Ajouter l'histogramme
        self.fig.add_trace(go.Bar(
            x=bin_centers,
            y=hist_counts,
            name='Distribution',
            marker=dict(
                color='#3498db',
                line=dict(color='#2980b9', width=1)
            ),
            hovertemplate='<b>Perte:</b> %{x:,.0f} FCFA<br><b>Fréquence:</b> %{y}<extra></extra>',
            opacity=0.8
        ))
        
        # Ajouter les seuils VaR
        mean = statistics['mean']
        var_95 = statistics['var_95']
        var_99 = statistics['var_99']
        
        # Ligne Moyenne (verte)
        self.fig.add_vline(
            x=mean,
            line_dash="solid",
            line_color="#2ecc71",
            line_width=3,
            annotation_text=f"Moy: {mean:,.0f}",
            annotation_position="top left",
            annotation_font=dict(size=10, color="#2ecc71")
        )
        
        # Ligne VaR 95% (orange)
        self.fig.add_vline(
            x=var_95,
            line_dash="dash",
            line_color="#f39c12",
            line_width=3,
            annotation_text=f"VaR95%: {var_95:,.0f}",
            annotation_position="bottom left",
            annotation_font=dict(size=10, color="#f39c12")
        )
        
        # Ligne VaR 99% (rouge)
        self.fig.add_vline(
            x=var_99,
            line_dash="dash",
            line_color="#e74c3c",
            line_width=3,
            annotation_text=f"VaR99%: {var_99:,.0f}",
            annotation_position="bottom right",
            annotation_font=dict(size=10, color="#e74c3c")
        )
        
        # Mise en forme
        self.fig.update_layout(
            title={
                'text': 'Distribution des Pertes - Simulation Monte Carlo',
                'font': {'size': 18, 'color': '#1F2937', 'family': 'Arial, sans-serif'},
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title='Pertes (FCFA)',
            yaxis_title='Fréquence',
            hovermode='x unified',
            template='plotly_white',
            height=650,
            width=1200,
            font=dict(size=12, family='Arial, sans-serif', color='#374151'),
            plot_bgcolor='#f9fafb',
            paper_bgcolor='#ffffff',
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#e5e7eb',
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#e5e7eb',
                zeroline=False
            ),
            margin=dict(l=80, r=80, t=100, b=80)
        )
        
        # Formatage des axes
        self.fig.update_xaxes(tickformat='.0f')
        self.fig.update_yaxes(tickformat='.0f')
        
        # Convertir en HTML
        html = self.fig.to_html(
            include_plotlyjs='cdn',
            div_id='histogram-chart'
        )
        
        return html
    
    def generate_box_plot(self, losses):
        """
        Génère un box plot interactif des pertes
        
        Args:
            losses: Array des pertes totales
        
        Returns:
            str: HTML du graphique Plotly
        """
        self.fig = go.Figure()
        
        self.fig.add_trace(go.Box(
            y=losses,
            name='Pertes',
            marker=dict(color='#3498db'),
            boxmean='sd',
            hovertemplate='<b>Perte:</b> %{y:,.0f} FCFA<extra></extra>',
            fillcolor='rgba(52, 152, 219, 0.7)',
            line=dict(color='#2980b9')
        ))
        
        self.fig.update_layout(
            title='Distribution des Pertes (Box Plot)',
            yaxis_title='Pertes (FCFA)',
            template='plotly_white',
            height=500,
            width=900,
            font=dict(size=12, family='Arial, sans-serif'),
            plot_bgcolor='#f9fafb',
            paper_bgcolor='#ffffff'
        )
        
        html = self.fig.to_html(
            include_plotlyjs='cdn',
            div_id='boxplot-chart'
        )
        
        return html
    
    def generate_density_plot(self, losses):
        """
        Génère un graphique de densité (KDE) interactif
        
        Args:
            losses: Array des pertes totales
        
        Returns:
            str: HTML du graphique Plotly
        """
        self.fig = go.Figure()
        
        # Histogramme
        self.fig.add_trace(go.Histogram(
            x=losses,
            name='Histogramme',
            nbinsx=50,
            marker=dict(color='#95a5a6', line=dict(color='#7f8c8d')),
            opacity=0.7,
            hovertemplate='<b>Plage:</b> %{x:,.0f} FCFA<br><b>Fréquence:</b> %{y}<extra></extra>'
        ))
        
        self.fig.update_layout(
            title='Distribution de Densité des Pertes',
            xaxis_title='Pertes (FCFA)',
            yaxis_title='Fréquence',
            template='plotly_white',
            height=550,
            width=1100,
            font=dict(size=12, family='Arial, sans-serif'),
            plot_bgcolor='#f9fafb',
            paper_bgcolor='#ffffff',
            hovermode='x'
        )
        
        html = self.fig.to_html(
            include_plotlyjs='cdn',
            div_id='density-chart'
        )
        
        return html
    
    def generate_comparison_chart(self, data_dict):
        """
        Génère un graphique de comparaison interactif
        
        Args:
            data_dict: Dict contenant {label: values} pour comparer
        
        Returns:
            str: HTML du graphique Plotly
        """
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        
        # Couleurs
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
        
        self.fig = go.Figure()
        
        self.fig.add_trace(go.Bar(
            x=labels,
            y=values,
            marker=dict(
                color=colors[:len(labels)],
                line=dict(color='#2c3e50', width=2)
            ),
            text=[f'{v:,.0f} FCFA' for v in values],
            textposition='outside',
            textfont=dict(size=12, color='#2c3e50'),
            hovertemplate='<b>%{x}</b><br>%{y:,.0f} FCFA<extra></extra>',
            opacity=0.9
        ))
        
        self.fig.update_layout(
            title='Comparaison des Indicateurs',
            yaxis_title='Montant (FCFA)',
            template='plotly_white',
            height=500,
            width=1000,
            font=dict(size=12, family='Arial, sans-serif'),
            plot_bgcolor='#f9fafb',
            paper_bgcolor='#ffffff',
            showlegend=False
        )
        
        html = self.fig.to_html(
            include_plotlyjs='cdn',
            div_id='comparison-chart'
        )
        
        return html
    
    def generate_summary_dashboard(self, losses, statistics):
        """
        Génère un dashboard complet avec plusieurs graphiques
        
        Args:
            losses: Array des pertes totales
            statistics: Dict contenant les statistiques
        
        Returns:
            str: HTML du dashboard complet
        """
        # Créer une figure avec subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Histogramme',
                'Box Plot',
                'Distribution Cumulée',
                'Comparaison Indicateurs'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'box'}],
                [{'type': 'scatter'}, {'type': 'bar'}]
            ]
        )
        
        # 1. Histogramme
        hist_counts, bin_edges = np.histogram(losses, bins=40)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        fig.add_trace(
            go.Bar(x=bin_centers, y=hist_counts, name='Distribution', marker_color='#3498db'),
            row=1, col=1
        )
        
        # 2. Box Plot
        fig.add_trace(
            go.Box(y=losses, name='Pertes', marker_color='#2ecc71'),
            row=1, col=2
        )
        
        # 3. Distribution Cumulée
        sorted_losses = np.sort(losses)
        cumulative = np.arange(1, len(sorted_losses) + 1) / len(sorted_losses)
        fig.add_trace(
            go.Scatter(x=sorted_losses, y=cumulative, mode='lines', name='CDF', 
                      line=dict(color='#e74c3c', width=2)),
            row=2, col=1
        )
        
        # 4. Comparaison
        comp_data = {
            'Moyenne': statistics['mean'],
            'Min': statistics['min'],
            'Max': statistics['max'],
            'VaR 95%': statistics['var_95']
        }
        fig.add_trace(
            go.Bar(x=list(comp_data.keys()), y=list(comp_data.values()),
                   marker_color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12']),
            row=2, col=2
        )
        
        # Mise en forme globale
        fig.update_layout(
            title_text='Dashboard de Simulation Monte Carlo',
            showlegend=False,
            height=900,
            width=1400,
            template='plotly_white',
            font=dict(size=11, family='Arial, sans-serif')
        )
        
        fig.update_xaxes(title_text='Pertes (FCFA)', row=1, col=1)
        fig.update_yaxes(title_text='Fréquence', row=1, col=1)
        fig.update_yaxes(title_text='Pertes (FCFA)', row=1, col=2)
        fig.update_xaxes(title_text='Pertes (FCFA)', row=2, col=1)
        fig.update_yaxes(title_text='Probabilité Cumulée', row=2, col=1)
        fig.update_xaxes(title_text='Indicateur', row=2, col=2)
        fig.update_yaxes(title_text='Montant (FCFA)', row=2, col=2)
        
        html = fig.to_html(
            include_plotlyjs='cdn',
            div_id='dashboard-chart'
        )
        
        return html


def generate_interactive_chart(losses, statistics):
    """
    Fonction utilitaire pour générer rapidement le graphique interactif principal
    
    Args:
        losses: Array des pertes totales
        statistics: Dict contenant les statistiques
    
    Returns:
        str: HTML du graphique Plotly
    """
    generator = InteractiveChartGenerator()
    return generator.generate_histogram(losses, statistics)
