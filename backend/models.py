#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèles SQLAlchemy pour la base de données SQLite
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    """Modèle utilisateur"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    simulations = db.relationship('Simulation', backref='user', lazy=True, cascade='all, delete-orphan')
    profiles = db.relationship('Profile', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Simulation(db.Model):
    """Modèle pour stocker les résultats de simulations"""
    __tablename__ = 'simulations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=True)
    
    # Paramètres de la simulation
    num_simulations = db.Column(db.Integer, nullable=False)
    sinistres_config = db.Column(db.JSON, nullable=False)  # Configuration des sinistres
    
    # Résultats
    statistics = db.Column(db.JSON, nullable=False)  # Stats globales
    statistics_by_type = db.Column(db.JSON, nullable=False)  # Stats par type
    histogram = db.Column(db.JSON, nullable=False)  # Données histogramme
    
    # Métadonnées
    name = db.Column(db.String(200), nullable=True)  # Nom de la simulation
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'profile_id': self.profile_id,
            'num_simulations': self.num_simulations,
            'sinistres_config': self.sinistres_config,
            'statistics': self.statistics,
            'statistics_by_type': self.statistics_by_type,
            'histogram': self.histogram,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Profile(db.Model):
    """Modèle pour les profils de simulation (configurations sauvegardées)"""
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    domain = db.Column(db.String(100), nullable=True)  # Domaine d'activité
    
    # Configuration par défaut
    default_num_simulations = db.Column(db.Integer, default=10000)
    sinistres_config = db.Column(db.JSON, nullable=False)  # Configuration des sinistres
    
    # Métadonnées
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    simulations = db.relationship('Simulation', backref='profile', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'domain': self.domain,
            'default_num_simulations': self.default_num_simulations,
            'sinistres_config': self.sinistres_config,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
