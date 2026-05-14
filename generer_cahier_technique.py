#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Cahier Technique PDF - Simulateur de Risques Financiers
Conforme aux normes UCAO-UUT
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from datetime import datetime

OUTPUT_FILE = "Cahier_Technique_Simulateur_Risque.pdf"

def create_pdf():
    doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    story = []
    styles = getSampleStyleSheet()
    
    # Styles personnalisés
    header_style = ParagraphStyle(name='Header', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#334155'), alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica')
    title_style = ParagraphStyle(name='CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#0F172A'), spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica-Bold')
    section_style = ParagraphStyle(name='SectionH', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1E293B'), spaceAfter=12, spaceBefore=12, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle(name='SubH', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#475569'), spaceAfter=10, fontName='Helvetica-Bold')
    body_style = ParagraphStyle(name='CustomBody', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#334155'), alignment=TA_JUSTIFY, spaceAfter=10)
    small_style = ParagraphStyle(name='SmallText', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#64748B'), alignment=TA_CENTER, spaceAfter=6)
    
    styles.add(header_style)
    styles.add(title_style)
    styles.add(section_style)
    styles.add(subtitle_style)
    styles.add(body_style)
    styles.add(small_style)
    
    # ===== PAGE 1 : PAGE DE GARDE =====
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("UNIVERSITÉ CATHOLIQUE DE L'AFRIQUE DE L'OUEST", header_style))
    story.append(Paragraph("Unité Universitaire du Togo — UCAO-UUT", header_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Foi  •  Science  •  Action</b>", small_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("SÉMINAIRE MIDA", header_style))
    story.append(Paragraph("MI = Mathématiques & Informatique   |   DA = Développement d'Applications", small_style))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("CAHIER TECHNIQUE", title_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Application Web :", header_style))
    story.append(Paragraph("Simulateur de Risques Financiers", title_style))
    story.append(Spacer(1, 1.5*cm))
    
    # Informations du projet
    story.append(Paragraph("INFORMATIONS DU PROJET", section_style))
    info_data = [
        ['Projet', 'Simulateur de Risques Financiers'],
        ['Type', 'Application Web (SPA)'],
        ['Version', 'v1.0.0'],
        ['Date', '27 avril 2026'],
        ['Groupe', 'Groupe 8 — Séminaire MIDA'],
        ['Encadrant', 'M. WOAMEY'],
        ['Statut', 'En développement'],
        ['Année académique', '2025 – 2026'],
        ['Localisation', 'Lomé, Togo']
    ]
    info_table = Table(info_data, colWidths=[4*cm, 11*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E2E8F0')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(info_table)
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("<i>UCAO-UUT  |  Unité Universitaire du Togo</i>", small_style))
    story.append(Paragraph("<i>Cahier Technique — Simulateur de Risques Financiers</i>", small_style))
    story.append(Paragraph("<i>UCAO-UUT  |  Séminaire MIDA  |  Groupe 8  |  Encadrant : M. WOAMEY  |  2025-2026</i>", small_style))
    story.append(PageBreak())
    
    # ===== TABLE DES MATIÈRES =====
    story.append(Paragraph("TABLE DES MATIÈRES", section_style))
    toc = """
    <b>1. Vue d'Ensemble</b><br/>
    <b>2. Architecture Générale</b><br/>
    <b>3. Frontend</b><br/>
    <b>4. Backend & API</b><br/>
    <b>5. Base de Données</b><br/>
    <b>6. Algorithmes & Simulations</b><br/>
    <b>7. Sécurité</b><br/>
    <b>8. Déploiement & Infrastructure</b><br/>
    <b>9. Maintenance & Monitoring</b><br/>
    <b>10. Glossaire</b><br/>
    <b>11. Conclusion</b>
    """
    story.append(Paragraph(toc, body_style))
    story.append(PageBreak())
    
    # ===== PAGE 2 : TITRE =====
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("SIMULATEUR DE RISQUES FINANCIERS", title_style))
    story.append(Paragraph("Cahier Technique Complet", subtitle_style))
    story.append(Spacer(1, 1*cm))
    
    info_data = [['Version', '1.0.0'], ['Date', datetime.now().strftime('%d/%m/%Y')], ['Auteur', 'MikeAlladoum'], ['Type', 'Documentation Technique']]
    info_table = Table(info_data, colWidths=[3*cm, 12*cm])
    info_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E2E8F0')), ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 10), ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))
    story.append(info_table)
    story.append(PageBreak())
    
    # ===== VUE D'ENSEMBLE =====
    story.append(Paragraph("1. VUE D'ENSEMBLE", section_style))
    story.append(Paragraph("Le <b>Simulateur de Risques Financiers</b> est une application web professionnelle dédiée à l'analyse et la simulation de risques financiers utilisant la méthode Monte Carlo.", body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # ===== ARCHITECTURE =====
    story.append(Paragraph("2. ARCHITECTURE GÉNÉRALE", section_style))
    story.append(Paragraph("L'application suit une architecture <b>SPA (Single Page Application)</b> avec séparation frontend-backend.", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    arch_data = [['Composant', 'Technologie', 'Rôle'], ['Frontend', 'JavaScript/HTML5/CSS3', 'Interface utilisateur'], ['Backend API', 'Python Flask', 'Logique métier'], ['Base de Données', 'SQLite/PostgreSQL', 'Persistance données'], ['Serveur', 'Vercel', 'Hébergement']]
    arch_table = Table(arch_data, colWidths=[3*cm, 4*cm, 8*cm])
    arch_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))
    story.append(arch_table)
    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())
    
    # ===== FRONTEND =====
    story.append(Paragraph("3. FRONTEND", section_style))
    story.append(Paragraph("3.1 Technologies", subtitle_style))
    frontend_text = "<b>Technologies:</b><br/>• HTML5 - Structure sémantique<br/>• CSS3 - Stylisation Flexbox/Grid<br/>• JavaScript (Vanilla) - Logique applicative<br/>• Plotly.js - Graphiques interactifs<br/><br/><b>Fonctionnalités:</b><br/>• Interface utilisateur responsive<br/>• Dashboard professionnel<br/>• Authentification sécurisée<br/>• Visualisations graphiques avancées"
    story.append(Paragraph(frontend_text, body_style))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("3.2 Structure", subtitle_style))
    files_text = "<b>Fichiers principaux:</b><br/>• index.html - Page principale<br/>• login.html - Authentification<br/>• main.css - Styles<br/>• js/app.js - Logique principale<br/>• js/auth.js - Gestion sessions<br/>• js/api.js - Appels backend<br/>• js/charts/ - Visualisations Plotly"
    story.append(Paragraph(files_text, body_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())
    
    # ===== BACKEND & API =====
    story.append(Paragraph("4. BACKEND & API", section_style))
    story.append(Paragraph("4.1 Technologies", subtitle_style))
    backend_text = "<b>Stack:</b><br/>• Python 3.8+<br/>• Flask (microframework)<br/>• SQLAlchemy (ORM)<br/>• NumPy/SciPy - Simulations<br/>• Pandas - Manipulation données<br/>• Matplotlib - Graphiques"
    story.append(Paragraph(backend_text, body_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("4.2 API REST Endpoints", subtitle_style))
    api_data = [['Endpoint', 'Méthode', 'Description'], ['/api/health', 'GET', 'Statut serveur'], ['/api/simulate', 'POST', 'Lance simulation'], ['/api/results', 'GET', 'Récupère résultats'], ['/api/auth/login', 'POST', 'Authentification'], ['/api/profiles', 'GET/POST', 'Profils utilisateurs'], ['/api/sinistres', 'GET/POST', 'Sinistres']]
    api_table = Table(api_data, colWidths=[3.5*cm, 2*cm, 7.5*cm])
    api_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 9), ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))
    story.append(api_table)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("4.3 Algorithme Monte Carlo", subtitle_style))
    monte_text = "L'algorithme utilise:<br/>• <b>Distributions:</b> Normale, Log-normale, Uniforme<br/>• <b>Itérations:</b> 10,000 simulations (configurable)<br/>• <b>Calculs:</b> Moyenne, écart-type, percentiles, VaR<br/>• <b>Visualisation:</b> Histogrammes, courbes cumulatives"
    story.append(Paragraph(monte_text, body_style))
    story.append(PageBreak())
    
    # ===== BASE DE DONNÉES =====
    story.append(Paragraph("5. BASE DE DONNÉES", section_style))
    story.append(Paragraph("5.1 Technologie", subtitle_style))
    db_text = "<b>SGBD Utilisé:</b> SQLite (développement) / PostgreSQL (production)<br/><b>ORM:</b> SQLAlchemy (abstraction base de données)<br/><b>Caractéristiques:</b><br/>• Stockage persistant utilisateurs<br/>• Archivage résultats simulations<br/>• Historique analyses<br/>• Gestion rôles et permissions"
    story.append(Paragraph(db_text, body_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("5.2 Tables Principales", subtitle_style))
    db_data = [['Table', 'Colonnes', 'Fonction'], ['users', 'id, username, email, password_hash, role', 'Gestion utilisateurs'], ['sessions', 'id, user_id, token, expires_at', 'Sessions actives'], ['simulations', 'id, user_id, params, results, created_at', 'Résultats'], ['profiles', 'id, user_id, name, risk_level, params', 'Profils'], ['sinistres', 'id, user_id, amount, date, category', 'Sinistres']]
    db_table = Table(db_data, colWidths=[2.5*cm, 5.5*cm, 6*cm])
    db_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('FONTSIZE', (0, 0), (-1, -1), 9), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))
    story.append(db_table)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("5.3 Sécurité Base de Données", subtitle_style))
    security_text = "• <b>Authentification:</b> Connexions sécurisées<br/>• <b>Chiffrement:</b> Hachage bcrypt mots de passe<br/>• <b>Requêtes paramétrées:</b> Protection injection SQL<br/>• <b>Backups:</b> Sauvegardes automatiques<br/>• <b>Isolation:</b> Chaque utilisateur accède ses données"
    story.append(Paragraph(security_text, body_style))
    story.append(PageBreak())
    
    # ===== DÉPLOIEMENT =====
    story.append(Paragraph("6. DÉPLOIEMENT & INFRASTRUCTURE", section_style))
    story.append(Paragraph("6.1 Vercel", subtitle_style))
    vercel_text = "<b>Frontend sur Vercel:</b><br/>• Déploiement automatique GitHub<br/>• HTTPS/TLS inclus<br/>• CDN global<br/>• Compression assets<br/><b>Avantages:</b><br/>• Déploiement < 2 minutes<br/>• Scalabilité automatique<br/>• Monitoring et analytics"
    story.append(Paragraph(vercel_text, body_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("6.2 Configuration", subtitle_style))
    config_text = "<b>vercel.json:</b><br/>• Routes SPA<br/>• Static builds<br/>• Headers CORS<br/>• Exclusion fichiers via .vercelignore"
    story.append(Paragraph(config_text, body_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())
    
    # ===== SÉCURITÉ =====
    story.append(Paragraph("7. SÉCURITÉ", section_style))
    security_full = """
    <b>7.1 Authentification:</b><br/>
    • JWT tokens<br/>
    • Hachage bcrypt<br/>
    • Système rôles<br/>
    <br/>
    <b>7.2 Communication:</b><br/>
    • HTTPS/TLS<br/>
    • Validation entrées<br/>
    • Protection CSRF<br/>
    <br/>
    <b>7.3 Données:</b><br/>
    • Chiffrement<br/>
    • Cookies HttpOnly<br/>
    • Rate limiting<br/>
    <br/>
    <b>7.4 Conformité:</b><br/>
    • RGPD<br/>
    • CNIL<br/>
    • ISO 27001
    """
    story.append(Paragraph(security_full, body_style))
    story.append(PageBreak())
    
    # ===== MAINTENANCE =====
    story.append(Paragraph("8. MAINTENANCE & MONITORING", section_style))
    maint_text = """
    <b>Monitoring:</b><br/>
    • Vercel Analytics<br/>
    • Error tracking<br/>
    • Uptime monitoring<br/>
    <br/>
    <b>Maintenance:</b><br/>
    • Updates dépendances mensuelles<br/>
    • Patches sécurité immédiats<br/>
    • Tests charge trimestriels<br/>
    • Audits annuels<br/>
    <br/>
    <b>Backup:</b><br/>
    • Sauvegardes quotidiennes<br/>
    • Replicas BD<br/>
    • RTO < 4h / RPO < 1h
    """
    story.append(Paragraph(maint_text, body_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())
    
    # ===== GLOSSAIRE =====
    story.append(Paragraph("9. GLOSSAIRE", section_style))
    glossary = [['Terme', 'Définition'], ['SPA', 'Single Page Application'], ['API', 'Application Programming Interface'], ['REST', 'Representational State Transfer'], ['JWT', 'JSON Web Token'], ['CORS', 'Cross-Origin Resource Sharing'], ['CDN', 'Content Delivery Network'], ['SGBD', 'Système Gestion Base Données'], ['ORM', 'Object-Relational Mapping'], ['VaR', 'Value at Risk'], ['RGPD', 'Réglement Protection Données'], ['PostgreSQL', 'Base données relationnelle']]
    glossary_table = Table(glossary, colWidths=[3*cm, 12*cm])
    glossary_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F59E0B')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('FONTSIZE', (0, 0), (-1, -1), 9), ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))
    story.append(glossary_table)
    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())
    
    # ===== CONCLUSION =====
    story.append(Paragraph("10. CONCLUSION", section_style))
    conclusion = """
    Le <b>Simulateur de Risques Financiers</b> est une application moderne, scalable et sécurisée conçue 
    pour l'analyse professionnelle de risques. Son architecture découplée permet une maintenance aisée et 
    une évolution continue. L'utilisation de technologies éprouvées et de meilleures pratiques garantit 
    la qualité et la fiabilité.<br/>
    <br/>
    L'application offre une expérience utilisateur fluide et intuitive tout en gérant efficacement les 
    complexités des simulations Monte Carlo. Avec son déploiement sur Vercel et sa base de données robuste 
    (SQLite/PostgreSQL), l'application est prête pour la production avec support professionnel et maintenance continue.
    """
    story.append(Paragraph(conclusion, body_style))
    story.append(Spacer(1, 1.5*cm))
    
    footer = f"<i>Généré: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Version 1.0.0 | © MikeAlladoum</i>"
    story.append(Paragraph(footer, body_style))
    
    doc.build(story)
    print(f"✅ PDF généré avec succès: {OUTPUT_FILE}")

if __name__ == '__main__':
    create_pdf()
