#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Cahier d'Analyse - Simulateur_de_Risque
Crée un PDF professionnel avec tous les aspects du projet
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os
from datetime import datetime

# Configuration
OUTPUT_FILE = "Cahier_Analyse_Simulateur_Risque.pdf"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = PROJECT_ROOT

# Styles personnalisés
def get_custom_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='Title_Custom',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Heading1_Custom',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Heading2_Custom',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='BodyText_Custom',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    ))
    
    return styles

def create_cover_page(story, styles):
    """Crée la page de couverture"""
    # En-tête UCAO
    header_data = [
        [Paragraph(
            "<b>UNIVERSITÉ CATHOLIQUE DE L'AFRIQUE DE L'OUEST</b><br/>"
            "Unité Universitaire du Togo — UCAO-UUT<br/>"
            "<i>Foi • Science • Action</i>",
            ParagraphStyle(
                'Header',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#0F172A'),
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
        )]
    ]
    header_table = Table(header_data, colWidths=[12*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E2E8F0')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#6366F1'))
    ]))
    story.append(header_table)
    story.append(Spacer(1, 1*cm))
    
    # Titre principal
    story.append(Paragraph("CAHIER D'ANALYSE", styles['Title_Custom']))
    story.append(Spacer(1, 0.5*cm))
    
    # Sous-titre
    story.append(Paragraph(
        "Simulateur de Risques Financiers",
        ParagraphStyle(
            'SubTitle',
            parent=styles['Normal'],
            fontSize=18,
            textColor=colors.HexColor('#6366F1'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
    ))
    
    story.append(Spacer(1, 1.5*cm))
    
    # Information du projet
    info_data = [
        ['Projet:', 'Simulateur de Risques Financiers v0.1'],
        ['Type:', 'Application Web'],
        ['Date:', datetime.now().strftime('%d/%m/%Y')],
        ['Auteur:', 'Équipe MIDA'],
        ['Status:', 'En Production']
    ]
    
    info_table = Table(info_data, colWidths=[2.5*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E2E8F0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1'))
    ]))
    
    story.append(info_table)
    story.append(PageBreak())

def create_table_of_contents(story, styles):
    """Crée la table des matières"""
    story.append(Paragraph("TABLE DES MATIÈRES", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.5*cm))
    
    contents = [
        "1. Objet du Système",
        "2. Architecture et Modules",
        "3. Modules et Fonctionnalités",
        "4. Acteurs et Utilisateurs",
        "5. Diagrammes de Cas d'Utilisation",
        "6. Diagrammes de Séquence",
        "7. Diagrammes de Classes",
        "8. Flux de Données",
        "9. Règles Métier et Gestion",
        "10. Conclusion"
    ]
    
    for item in contents:
        story.append(Paragraph(f"• {item}", styles['BodyText_Custom']))
        story.append(Spacer(1, 0.2*cm))
    
    story.append(PageBreak())

def add_section_1_object(story, styles):
    """Objet du Système"""
    story.append(Paragraph("1. OBJET DU SYSTÈME", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    content = """
    Le Simulateur de Risques Financiers est une application web permettant aux entreprises 
    d'évaluer et de simuler les risques de pertes financières selon des modèles statistiques 
    avancés. Le système utilise la simulation Monte Carlo pour générer des scénarios d'exposition 
    aux risques et fournir des statistiques détaillées.
    """
    
    story.append(Paragraph(content.strip(), styles['BodyText_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    # Objectifs
    story.append(Paragraph("Objectifs Principaux:", styles['Heading2_Custom']))
    objectives = [
        "Simuler les risques de sinistralité selon des distributions statistiques",
        "Calculer des métriques de risque (VaR, CVaR, quantiles)",
        "Fournir une visualisation interactive des résultats",
        "Supporter plusieurs devises (FCFA, USD, EUR)",
        "Assurer la performance pour simulations massives (jusqu'à 1M scénarios)",
        "Offrir une interface moderne et ergonomique"
    ]
    
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", styles['BodyText_Custom']))
        story.append(Spacer(1, 0.1*cm))
    
    story.append(PageBreak())

def add_section_2_architecture(story, styles):
    """Architecture et Modules"""
    story.append(Paragraph("2. ARCHITECTURE ET MODULES", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    content = """
    L'application suit une architecture client-serveur avec séparation des responsabilités:
    """
    story.append(Paragraph(content, styles['BodyText_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    # Architecture table - améliorée
    arch_data = [
        [
            Paragraph("<b>COUCHE</b>", styles['BodyText_Custom']),
            Paragraph("<b>TECHNOLOGIES</b>", styles['BodyText_Custom']),
            Paragraph("<b>RESPONSABILITÉS</b>", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Présentation", styles['BodyText_Custom']),
            Paragraph("HTML5<br/>CSS3<br/>JavaScript", styles['BodyText_Custom']),
            Paragraph("• Interface utilisateur moderne<br/>• Validation côté client<br/>• Visualisation des résultats", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Application", styles['BodyText_Custom']),
            Paragraph("Flask 2.3.3<br/>Python 3.11+", styles['BodyText_Custom']),
            Paragraph("• API REST<br/>• Orchestration des requêtes<br/>• Gestion des transactions", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Métier", styles['BodyText_Custom']),
            Paragraph("Python 3.11+<br/>NumPy 1.25+<br/>Plotly 5.17+", styles['BodyText_Custom']),
            Paragraph("• Simulation Monte Carlo<br/>• Calculs statistiques<br/>• Génération de graphiques", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Données", styles['BodyText_Custom']),
            Paragraph("JSON<br/>En mémoire", styles['BodyText_Custom']),
            Paragraph("• Stockage temporaire<br/>• Cache de simulations<br/>• Historique de session", styles['BodyText_Custom'])
        ]
    ]
    
    arch_table = Table(arch_data, colWidths=[2.5*cm, 3.5*cm, 6.5*cm])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366F1')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    story.append(arch_table)
    story.append(Spacer(1, 0.3*cm))
    story.append(PageBreak())

def add_section_3_modules(story, styles):
    """Modules et Fonctionnalités"""
    story.append(Paragraph("3. MODULES ET FONCTIONNALITÉS", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    # Tableau récapitulatif des modules
    story.append(Paragraph("3.0 Récapitulatif des Modules et Fonctionnalités", styles['Heading2_Custom']))
    story.append(Spacer(1, 0.2*cm))
    
    modules_data = [
        [
            Paragraph("<b>MODULE</b>", styles['BodyText_Custom']),
            Paragraph("<b>TYPE</b>", styles['BodyText_Custom']),
            Paragraph("<b>DESCRIPTION</b>", styles['BodyText_Custom']),
            Paragraph("<b>FONCTIONNALITÉS CLÉS</b>", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Monte Carlo", styles['BodyText_Custom']),
            Paragraph("Fonctionnalité", styles['BodyText_Custom']),
            Paragraph("Moteur de simulation stochastique", styles['BodyText_Custom']),
            Paragraph("• Simulation<br/>• Run<br/>• Get Losses<br/>• Histogram Data", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Statistics", styles['BodyText_Custom']),
            Paragraph("Fonctionnalité", styles['BodyText_Custom']),
            Paragraph("Calcul des métriques de risque", styles['BodyText_Custom']),
            Paragraph("• Calculate All<br/>• To Dict<br/>• VaR<br/>• CVaR", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Validators", styles['BodyText_Custom']),
            Paragraph("Fonctionnalité", styles['BodyText_Custom']),
            Paragraph("Validation des paramètres d'entrée", styles['BodyText_Custom']),
            Paragraph("• Validate Lambda<br/>• Validate Mu<br/>• Validate N", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Chart Generator", styles['BodyText_Custom']),
            Paragraph("Fonctionnalité", styles['BodyText_Custom']),
            Paragraph("Génération des visualisations", styles['BodyText_Custom']),
            Paragraph("• Generate Histogram<br/>• Format Data<br/>• Export HTML", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Cache Manager", styles['BodyText_Custom']),
            Paragraph("Vue/Optimisation", styles['BodyText_Custom']),
            Paragraph("Mise en cache des simulations", styles['BodyText_Custom']),
            Paragraph("• Get Cache<br/>• Set Cache<br/>• Get Stats", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Performance Monitor", styles['BodyText_Custom']),
            Paragraph("Vue/Monitoring", styles['BodyText_Custom']),
            Paragraph("Suivi des performances", styles['BodyText_Custom']),
            Paragraph("• Record Metrics<br/>• Get Performance<br/>• Get Slowest", styles['BodyText_Custom'])
        ]
    ]
    
    modules_table = Table(modules_data, colWidths=[2.2*cm, 2*cm, 3.2*cm, 4.6*cm])
    modules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366F1')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    story.append(modules_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Module 1: Monte Carlo
    story.append(Paragraph("3.1 Module: Simulation Monte Carlo", styles['Heading2_Custom']))
    content_mc = """
    <b>Type:</b> Fonctionnalité Métier<br/>
    <b>Responsabilité:</b> Génération de scénarios aléatoires et calcul des pertes totales
    """
    story.append(Paragraph(content_mc, styles['BodyText_Custom']))
    
    functions_mc = [
        ("simulate()", "Exécute la simulation complète"),
        ("run()", "Alias pour simulate()"),
        ("get_losses()", "Retourne l'array des pertes"),
        ("get_histogram_data(bins)", "Génère les données d'histogramme")
    ]
    
    for func, desc in functions_mc:
        story.append(Paragraph(f"• <b>{func}:</b> {desc}", styles['BodyText_Custom']))
    
    story.append(Spacer(1, 0.3*cm))
    
    # Module 2: Statistics
    story.append(Paragraph("3.2 Module: Calculs Statistiques", styles['Heading2_Custom']))
    content_stat = """
    <b>Type:</b> Fonctionnalité Métier<br/>
    <b>Responsabilité:</b> Calcul des métriques de risque
    """
    story.append(Paragraph(content_stat, styles['BodyText_Custom']))
    
    functions_stat = [
        ("calculate_all()", "Calcule toutes les métriques"),
        ("to_dict()", "Sérialise les résultats en JSON"),
        ("mean, median, std, min, max", "Statistiques descriptives"),
        ("VaR(95%, 99%)", "Value at Risk"),
        ("CVaR(95%, 99%)", "Conditional Value at Risk"),
        ("num_zero_loss", "Nombre de scénarios sans perte")
    ]
    
    for func, desc in functions_stat:
        story.append(Paragraph(f"• <b>{func}:</b> {desc}", styles['BodyText_Custom']))
    
    story.append(Spacer(1, 0.3*cm))
    
    # Module 3: Validation
    story.append(Paragraph("3.3 Module: Validation des Paramètres", styles['Heading2_Custom']))
    content_val = """
    <b>Type:</b> Fonctionnalité Métier<br/>
    <b>Responsabilité:</b> Validation des entrées utilisateur
    """
    story.append(Paragraph(content_val, styles['BodyText_Custom']))
    
    constraints = [
        [Paragraph("<b>Paramètre</b>", styles['BodyText_Custom']), Paragraph("<b>Plage</b>", styles['BodyText_Custom']), Paragraph("<b>Description</b>", styles['BodyText_Custom'])],
        [Paragraph("Lambda (λ)", styles['BodyText_Custom']), Paragraph("0.01 - 1000", styles['BodyText_Custom']), Paragraph("Paramètre Poisson (fréquence)", styles['BodyText_Custom'])],
        [Paragraph("Mu (μ)", styles['BodyText_Custom']), Paragraph("0.01 - 1000000", styles['BodyText_Custom']), Paragraph("Paramètre Exponentielle (sévérité)", styles['BodyText_Custom'])],
        [Paragraph("Simulations (N)", styles['BodyText_Custom']), Paragraph("100 - 1000000", styles['BodyText_Custom']), Paragraph("Nombre de scénarios à simuler", styles['BodyText_Custom'])]
    ]
    
    const_table = Table(constraints, colWidths=[3*cm, 3*cm, 6*cm])
    const_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    story.append(const_table)
    story.append(Spacer(1, 0.3*cm))
    
    # Module 4: Charts
    story.append(Paragraph("3.4 Module: Génération de Visualisations", styles['Heading2_Custom']))
    content_chart = """
    <b>Type:</b> Fonctionnalité Présentation<br/>
    <b>Responsabilité:</b> Création des graphiques interactifs Plotly<br/>
    <b>Fonction:</b> generate_histogram() - Crée un histogramme interactif
    """
    story.append(Paragraph(content_chart, styles['BodyText_Custom']))
    
    story.append(Spacer(1, 0.5*cm))
    
    # Module 5: Sinistres Multiples
    story.append(Paragraph("3.5 Module: Gestion des Sinistres Multiples", styles['Heading2_Custom']))
    content_sinistres = """
    <b>Type:</b> Fonctionnalité Métier Avancée<br/>
    <b>Responsabilité:</b> Support pour plusieurs types de sinistres avec coûts différents<br/>
    <b>Amélioration v0.2:</b> Permet l'analyse granulaire des risques par type
    """
    story.append(Paragraph(content_sinistres, styles['BodyText_Custom']))
    
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>Types de Sinistres Supportés (Exemple - Assurance Santé):</b>", styles['BodyText_Custom']))
    
    sinistres_types = [
        [Paragraph("<b>Type</b>", styles['BodyText_Custom']), Paragraph("<b>Fréquence (λ)</b>", styles['BodyText_Custom']), Paragraph("<b>Coût Moyen</b>", styles['BodyText_Custom']), Paragraph("<b>Description</b>", styles['BodyText_Custom'])],
        [Paragraph("Consultation", styles['BodyText_Custom']), Paragraph("2.0", styles['BodyText_Custom']), Paragraph("5 000 FCFA", styles['BodyText_Custom']), Paragraph("Visite médicale standard", styles['BodyText_Custom'])],
        [Paragraph("Hospitalisation", styles['BodyText_Custom']), Paragraph("0.3", styles['BodyText_Custom']), Paragraph("250 000 FCFA", styles['BodyText_Custom']), Paragraph("Séjour hospitalier", styles['BodyText_Custom'])],
        [Paragraph("Chirurgie", styles['BodyText_Custom']), Paragraph("0.1", styles['BodyText_Custom']), Paragraph("1 000 000 FCFA", styles['BodyText_Custom']), Paragraph("Intervention chirurgicale", styles['BodyText_Custom'])],
        [Paragraph("Médicaments", styles['BodyText_Custom']), Paragraph("1.5", styles['BodyText_Custom']), Paragraph("30 000 FCFA", styles['BodyText_Custom']), Paragraph("Ordonnances et traitements", styles['BodyText_Custom'])]
    ]
    
    sinistres_table = Table(sinistres_types, colWidths=[2.5*cm, 2*cm, 2.5*cm, 4*cm])
    sinistres_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    story.append(sinistres_table)
    story.append(Spacer(1, 0.3*cm))
    
    # Caractéristiques
    story.append(Paragraph("<b>Caractéristiques:</b>", styles['BodyText_Custom']))
    features = [
        "• Configuration flexible des sinistres (λ et coût moyen personnalisables)",
        "• Simulation simultanée de plusieurs types de risques",
        "• Analyse d'impact par type de sinistre (contribution au risque total)",
        "• Statistiques détaillées pour chaque type (min, max, moyenne)",
        "• Rapport consolidé avec distribution des pertes globales"
    ]
    
    for feature in features:
        story.append(Paragraph(feature, styles['BodyText_Custom']))
    
    story.append(PageBreak())

def add_section_4_actors(story, styles):
    """Acteurs et Utilisateurs"""
    story.append(Paragraph("4. ACTEURS ET UTILISATEURS", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    actors_data = [
        [
            Paragraph("<b>ACTEUR</b>", styles['BodyText_Custom']),
            Paragraph("<b>RÔLE</b>", styles['BodyText_Custom']),
            Paragraph("<b>RESPONSABILITÉS</b>", styles['BodyText_Custom']),
            Paragraph("<b>ACTIONS PRINCIPALES</b>", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Analyste Risque", styles['BodyText_Custom']),
            Paragraph("Utilisateur Principal", styles['BodyText_Custom']),
            Paragraph("Effectuer des simulations<br/>Analyser les résultats", styles['BodyText_Custom']),
            Paragraph("• Créer simulations<br/>• Interpréter résultats<br/>• Exporter rapports", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Responsable Risque", styles['BodyText_Custom']),
            Paragraph("Superviseur", styles['BodyText_Custom']),
            Paragraph("Valider les analyses<br/>Approuver décisions", styles['BodyText_Custom']),
            Paragraph("• Consulter résultats<br/>• Valider analyses<br/>• Approuver actions", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Administrateur", styles['BodyText_Custom']),
            Paragraph("Responsable Technique", styles['BodyText_Custom']),
            Paragraph("Maintenir infrastructure<br/>Gérer sécurité", styles['BodyText_Custom']),
            Paragraph("• Maintenir serveurs<br/>• Gérer données<br/>• Assurer sécurité", styles['BodyText_Custom'])
        ],
        [
            Paragraph("Système API", styles['BodyText_Custom']),
            Paragraph("Acteur Technique", styles['BodyText_Custom']),
            Paragraph("Traiter les requêtes<br/>Exécuter calculs", styles['BodyText_Custom']),
            Paragraph("• Valider paramètres<br/>• Exécuter simulations<br/>• Retourner résultats", styles['BodyText_Custom'])
        ]
    ]
    
    actors_table = Table(actors_data, colWidths=[2*cm, 2.2*cm, 3.3*cm, 3.5*cm])
    actors_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#A855F7')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    story.append(actors_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Use Cases
    story.append(Paragraph("Cas d'Utilisation Principaux:", styles['Heading2_Custom']))
    usecases = [
        "UC1: Créer une nouvelle simulation",
        "UC2: Visualiser les résultats",
        "UC3: Exporter les statistiques",
        "UC4: Comparer plusieurs scénarios",
        "UC5: Consulter l'historique des simulations"
    ]
    
    for uc in usecases:
        story.append(Paragraph(f"• {uc}", styles['BodyText_Custom']))
    
    story.append(PageBreak())

def add_section_4_authentication(story, styles):
    """Authentification et Sécurité"""
    story.append(Paragraph("4. AUTHENTIFICATION ET SÉCURITÉ", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("4.1 Système d'Authentification JWT", styles['Heading2_Custom']))
    auth_intro = """
    <b>Type:</b> Fonctionnalité Sécurité<br/>
    <b>Framework:</b> Flask-JWT-Extended v4.5.2<br/>
    <b>Modèle:</b> Stateless avec tokens JWT (JSON Web Tokens)
    """
    story.append(Paragraph(auth_intro, styles['BodyText_Custom']))
    
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>Endpoints d'Authentification:</b>", styles['BodyText_Custom']))
    
    auth_endpoints = [
        [Paragraph("<b>Endpoint</b>", styles['BodyText_Custom']), Paragraph("<b>Méthode</b>", styles['BodyText_Custom']), Paragraph("<b>Description</b>", styles['BodyText_Custom'])],
        [Paragraph("/api/auth/login", styles['BodyText_Custom']), Paragraph("POST", styles['BodyText_Custom']), Paragraph("Authentifie l'utilisateur et génère un JWT", styles['BodyText_Custom'])],
        [Paragraph("/api/auth/logout", styles['BodyText_Custom']), Paragraph("POST", styles['BodyText_Custom']), Paragraph("Déconnexion (gestion client-side)", styles['BodyText_Custom'])],
        [Paragraph("/api/simulate", styles['BodyText_Custom']), Paragraph("POST", styles['BodyText_Custom']), Paragraph("Endpoint protégé - requiert Bearer token", styles['BodyText_Custom'])]
    ]
    
    auth_table = Table(auth_endpoints, colWidths=[3*cm, 2*cm, 6*cm])
    auth_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    story.append(auth_table)
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("<b>Flux d'Authentification:</b>", styles['BodyText_Custom']))
    auth_flow = [
        "1. L'utilisateur soumet username/password au endpoint /api/auth/login",
        "2. Le serveur valide les credentials contre la base de données de démo",
        "3. Un JWT valide pour 24 heures est généré et retourné au client",
        "4. Le client stocke le token en localStorage",
        "5. Pour les requêtes protégées, le token est envoyé dans le header Authorization: Bearer {token}",
        "6. Le serveur valide le token avant d'exécuter la simulation"
    ]
    
    for step in auth_flow:
        story.append(Paragraph(f"• {step}", styles['BodyText_Custom']))
    
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("<b>Utilisateurs Démo Disponibles:</b>", styles['BodyText_Custom']))
    
    demo_users = [
        [Paragraph("<b>Utilisateur</b>", styles['BodyText_Custom']), Paragraph("<b>Mot de passe</b>", styles['BodyText_Custom']), Paragraph("<b>Rôle</b>", styles['BodyText_Custom'])],
        [Paragraph("demo", styles['BodyText_Custom']), Paragraph("demo123", styles['BodyText_Custom']), Paragraph("Utilisateur de test", styles['BodyText_Custom'])],
        [Paragraph("admin", styles['BodyText_Custom']), Paragraph("admin123", styles['BodyText_Custom']), Paragraph("Administrateur", styles['BodyText_Custom'])],
        [Paragraph("user1", styles['BodyText_Custom']), Paragraph("password1", styles['BodyText_Custom']), Paragraph("Utilisateur standard", styles['BodyText_Custom'])]
    ]
    
    demo_table = Table(demo_users, colWidths=[3*cm, 3*cm, 4*cm])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F59E0B')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    story.append(demo_table)
    
    story.append(PageBreak())

def add_section_5_usecase_diagram(story, styles):
    """Diagrammes de Cas d'Utilisation"""
    story.append(Paragraph("5. DIAGRAMMES DE CAS D'UTILISATION", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "Le diagramme ci-dessous représente les interactions entre les acteurs et les cas d'utilisation du système:",
        styles['BodyText_Custom']
    ))
    story.append(Spacer(1, 0.3*cm))
    
    # Ajouter l'image du diagramme
    image_path = os.path.join(IMAGES_DIR, "diagrammes_cas_d'utilisation.png")
    if os.path.exists(image_path):
        try:
            img = Image(image_path, width=6*inch, height=4*inch)
            story.append(img)
        except:
            story.append(Paragraph(
                "Image non disponible: diagrammes_cas_d'utilisation.png",
                styles['BodyText_Custom']
            ))
    else:
        story.append(Paragraph(
            "Image non disponible: diagrammes_cas_d'utilisation.png",
            styles['BodyText_Custom']
        ))
    
    story.append(PageBreak())

def add_section_6_sequence_diagram(story, styles):
    """Diagrammes de Séquence"""
    story.append(Paragraph("6. DIAGRAMMES DE SÉQUENCE", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "Ce diagramme illustre la séquence d'interactions pour le cas d'utilisation principal: Exécuter une simulation",
        styles['BodyText_Custom']
    ))
    story.append(Spacer(1, 0.3*cm))
    
    # Ajouter l'image
    image_path = os.path.join(IMAGES_DIR, "diagrammes_sequence.png")
    if os.path.exists(image_path):
        try:
            img = Image(image_path, width=6*inch, height=4*inch)
            story.append(img)
        except:
            story.append(Paragraph(
                "Image non disponible: diagrammes_sequence.png",
                styles['BodyText_Custom']
            ))
    else:
        story.append(Paragraph(
            "Image non disponible: diagrammes_sequence.png",
            styles['BodyText_Custom']
        ))
    
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "<b>Flux de la séquence:</b><br/>"
        "1. L'utilisateur soumet un formulaire avec les paramètres<br/>"
        "2. Le frontend valide les données<br/>"
        "3. La requête est envoyée au serveur API<br/>"
        "4. L'API valide les paramètres côté serveur<br/>"
        "5. Le moteur Monte Carlo exécute la simulation<br/>"
        "6. Les statistiques sont calculées<br/>"
        "7. Un graphique est généré<br/>"
        "8. Les résultats sont retournés au client<br/>"
        "9. L'interface affiche les résultats et le graphique",
        styles['BodyText_Custom']
    ))
    
    story.append(PageBreak())

def add_section_7_class_diagram(story, styles):
    """Diagrammes de Classes"""
    story.append(Paragraph("7. DIAGRAMMES DE CLASSES", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "Le diagramme de classes représente la structure des principaux objets du système:",
        styles['BodyText_Custom']
    ))
    story.append(Spacer(1, 0.3*cm))
    
    # Ajouter l'image
    image_path = os.path.join(IMAGES_DIR, "diagrammes_des_classes .png")
    if os.path.exists(image_path):
        try:
            img = Image(image_path, width=6*inch, height=4.5*inch)
            story.append(img)
        except:
            story.append(Paragraph(
                "Image non disponible: diagrammes_des_classes.png",
                styles['BodyText_Custom']
            ))
    else:
        story.append(Paragraph(
            "Image non disponible: diagrammes_des_classes.png",
            styles['BodyText_Custom']
        ))
    
    story.append(Spacer(1, 0.3*cm))
    
    # Descriptions des classes
    story.append(Paragraph("<b>Classes Principales:</b>", styles['Heading2_Custom']))
    
    classes_info = [
        ("MonteCarlo", "Classe responsable de la simulation. Utilise les distributions Poisson et Exponentielle pour générer des scénarios."),
        ("StatisticsCalculator", "Classe de calcul des métriques statistiques (moyenne, médiane, VaR, CVaR, etc.)."),
        ("InteractiveChartGenerator", "Classe de génération des visualisations Plotly."),
        ("SimulationCache", "Classe de mise en cache pour optimiser les requêtes répétitives."),
        ("PerformanceMonitor", "Classe de suivi des performances et des métriques d'exécution.")
    ]
    
    for class_name, description in classes_info:
        story.append(Paragraph(f"• <b>{class_name}:</b> {description}", styles['BodyText_Custom']))
        story.append(Spacer(1, 0.1*cm))
    
    story.append(PageBreak())

def add_section_8_data_flow(story, styles):
    """Flux de Données"""
    story.append(Paragraph("8. FLUX DE DONNÉES", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "Le diagramme de flux de données ci-dessous représente le flux d'information à travers les différentes couches du système et le cycle complet d'une simulation:",
        styles['BodyText_Custom']
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Ajouter l'image avec une taille généreuse
    image_path = os.path.join(IMAGES_DIR, "diagramme_flux.jpeg")
    if os.path.exists(image_path):
        try:
            img = Image(image_path, width=7*inch, height=5.5*inch)
            story.append(img)
        except:
            story.append(Paragraph(
                "Image non disponible: diagramme_flux.jpeg",
                styles['BodyText_Custom']
            ))
    else:
        story.append(Paragraph(
            "Image non disponible: diagramme_flux.jpeg",
            styles['BodyText_Custom']
        ))
    
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("<b>Description détaillée du flux:</b>", styles['Heading2_Custom']))
    
    flux_data = [
        [
            Paragraph("<b>ÉTAPE</b>", styles['BodyText_Custom']),
            Paragraph("<b>ACTION</b>", styles['BodyText_Custom']),
            Paragraph("<b>COMPOSANTS</b>", styles['BodyText_Custom']),
            Paragraph("<b>RÉSULTAT</b>", styles['BodyText_Custom'])
        ],
        [
            Paragraph("1", styles['BodyText_Custom']),
            Paragraph("Entrée", styles['BodyText_Custom']),
            Paragraph("Formulaire Frontend", styles['BodyText_Custom']),
            Paragraph("Paramètres (λ, μ, N)", styles['BodyText_Custom'])
        ],
        [
            Paragraph("2", styles['BodyText_Custom']),
            Paragraph("Validation", styles['BodyText_Custom']),
            Paragraph("Validators Module", styles['BodyText_Custom']),
            Paragraph("Paramètres validés", styles['BodyText_Custom'])
        ],
        [
            Paragraph("3", styles['BodyText_Custom']),
            Paragraph("Simulation", styles['BodyText_Custom']),
            Paragraph("MonteCarlo Engine", styles['BodyText_Custom']),
            Paragraph("Array de pertes", styles['BodyText_Custom'])
        ],
        [
            Paragraph("4", styles['BodyText_Custom']),
            Paragraph("Calcul", styles['BodyText_Custom']),
            Paragraph("StatisticsCalculator", styles['BodyText_Custom']),
            Paragraph("Métriques (VaR, CVaR)", styles['BodyText_Custom'])
        ],
        [
            Paragraph("5", styles['BodyText_Custom']),
            Paragraph("Visualisation", styles['BodyText_Custom']),
            Paragraph("ChartGenerator", styles['BodyText_Custom']),
            Paragraph("Histogramme HTML", styles['BodyText_Custom'])
        ],
        [
            Paragraph("6", styles['BodyText_Custom']),
            Paragraph("Sortie", styles['BodyText_Custom']),
            Paragraph("API Response", styles['BodyText_Custom']),
            Paragraph("JSON résultats complets", styles['BodyText_Custom'])
        ]
    ]
    
    flux_table = Table(flux_data, colWidths=[1*cm, 2*cm, 3*cm, 4*cm])
    flux_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366F1')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    
    story.append(flux_table)
    story.append(PageBreak())

def add_section_9_rules_management(story, styles):
    """Règles Métier et Gestion"""
    story.append(Paragraph("9. RÈGLES MÉTIER ET GESTION", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    # Règles Métier
    story.append(Paragraph("9.1 Règles Métier", styles['Heading2_Custom']))
    
    rules = [
        ("RM01", "Les paramètres lambda et mu doivent être > 0"),
        ("RM02", "Le nombre de simulations doit être ≥ 100 et ≤ 1 000 000"),
        ("RM03", "Lambda doit être ≤ 1000"),
        ("RM04", "Mu doit être ≤ 1 000 000"),
        ("RM05", "Tous les paramètres sont obligatoires"),
        ("RM06", "Les résultats doivent inclure min, max, moyen, médiane, std"),
        ("RM07", "VaR et CVaR doivent être calculés à 95% et 99%"),
        ("RM08", "Le système doit traiter jusqu'à 1 million de scénarios")
    ]
    
    rules_table = Table(rules, colWidths=[1.5*cm, 12*cm])
    rules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366F1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1'))
    ]))
    
    story.append(rules_table)
    story.append(Spacer(1, 0.3*cm))
    
    # Gestion des Erreurs
    story.append(Paragraph("9.2 Gestion des Erreurs", styles['Heading2_Custom']))
    
    errors = [
        ("Validation échouée", "400 Bad Request - Message d'erreur détaillé"),
        ("Paramètre invalide", "400 Bad Request - Description de la contrainte violée"),
        ("Serveur non disponible", "503 Service Unavailable"),
        ("Erreur interne", "500 Internal Server Error")
    ]
    
    errors_table = Table(errors, colWidths=[4*cm, 10*cm])
    errors_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EF4444')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1'))
    ]))
    
    story.append(errors_table)
    story.append(Spacer(1, 0.3*cm))
    
    # Gestion de la Sécurité
    story.append(Paragraph("9.3 Gestion de la Sécurité", styles['Heading2_Custom']))
    
    security = [
        "• CORS (Cross-Origin Resource Sharing) activé",
        "• Validation stricte des entrées côté serveur",
        "• Validation côté client pour meilleure UX",
        "• Pas de stockage permanent des données sensibles",
        "• Communication HTTPS recommandée en production"
    ]
    
    for item in security:
        story.append(Paragraph(item, styles['BodyText_Custom']))
    
    story.append(PageBreak())

def add_section_10_conclusion(story, styles):
    """Conclusion"""
    story.append(Paragraph("10. CONCLUSION", styles['Heading1_Custom']))
    story.append(Spacer(1, 0.3*cm))
    
    conclusion = """
    Le Simulateur de Risques Financiers est une application bien structurée, modulaire et 
    scalable. Son architecture client-serveur permet une séparation claire des responsabilités, 
    facilitant la maintenance et l'évolution future.<br/><br/>
    
    <b>Forces du système:</b><br/>
    • Architecture modulaire et maintenable<br/>
    • Performance optimisée pour simulations massives<br/>
    • Interface utilisateur moderne et responsive<br/>
    • Validation robuste des données<br/>
    • Visualisations interactives<br/>
    • Support multi-devise<br/><br/>
    
    <b>Points à améliorer (v0.2+):</b><br/>
    • Implémentation d'une base de données persistante<br/>
    • Historique des simulations utilisateur<br/>
    • Authentification et autorisation<br/>
    • Export en multiple formats (PDF, Excel)<br/>
    • API documentation (Swagger/OpenAPI)<br/>
    • Tests unitaires exhaustifs<br/>
    • Containerization Docker<br/>
    • Déploiement continu (CI/CD)<br/><br/>
    
    Le système est prêt pour une utilisation en production et peut facilement être étendu 
    pour supporter de nouvelles distributions statistiques et métriques de risque.
    """
    
    story.append(Paragraph(conclusion, styles['BodyText_Custom']))
    story.append(Spacer(1, 0.5*cm))
    
    # Footer
    story.append(Paragraph(
        f"Document généré le: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#94A3B8'),
            alignment=TA_CENTER
        )
    ))

def main():
    """Fonction principale"""
    print("Generation du cahier d'analyse...")
    
    # Créer le document PDF
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Récupérer les styles
    styles = get_custom_styles()
    
    # Story (contenu du PDF)
    story = []
    
    # Ajouter les sections
    create_cover_page(story, styles)
    create_table_of_contents(story, styles)
    add_section_1_object(story, styles)
    add_section_2_architecture(story, styles)
    add_section_3_modules(story, styles)
    add_section_4_authentication(story, styles)
    add_section_4_actors(story, styles)
    add_section_5_usecase_diagram(story, styles)
    add_section_6_sequence_diagram(story, styles)
    add_section_7_class_diagram(story, styles)
    add_section_8_data_flow(story, styles)
    add_section_9_rules_management(story, styles)
    add_section_10_conclusion(story, styles)
    
    # Générer le PDF
    try:
        doc.build(story)
        print(f"Cahier d'analyse genere avec succes!")
        print(f"Fichier: {OUTPUT_FILE}")
        print(f"Localisation: {os.path.abspath(OUTPUT_FILE)}")
        return True
    except Exception as e:
        print(f"Erreur lors de la generation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
