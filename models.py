"""
Database models for Medicino application.
SQLAlchemy ORM models with proper relationships and validation.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    diagnosis_history = db.relationship('DiagnosisHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    @validates('email')
    def validate_email(self, key, email):
        """Validate email format."""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email.lower()
    
    @property
    def password(self):
        """Password property - cannot be read."""
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    @hybrid_property
    def full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Medicine(db.Model):
    """Medicine model for storing medicine information."""
    
    __tablename__ = 'medicines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    dosage = db.Column(db.Text)
    side_effects = db.Column(db.Text)
    contraindications = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    category = db.Column(db.String(100), index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert medicine to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'dosage': self.dosage,
            'side_effects': self.side_effects,
            'contraindications': self.contraindications,
            'price': float(self.price) if self.price else None,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Medicine {self.name}>'

class Condition(db.Model):
    """Medical condition model."""
    
    __tablename__ = 'conditions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text, nullable=False)
    ayurvedic_remedy = db.Column(db.Text)
    modern_treatment = db.Column(db.Text)
    severity_level = db.Column(db.String(20), default='moderate')
    category = db.Column(db.String(100), index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert condition to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'symptoms': self.symptoms,
            'ayurvedic_remedy': self.ayurvedic_remedy,
            'modern_treatment': self.modern_treatment,
            'severity_level': self.severity_level,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Condition {self.name}>'

class DiagnosisHistory(db.Model):
    """Diagnosis history model for tracking user diagnoses."""
    
    __tablename__ = 'diagnosis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    symptoms = db.Column(db.Text, nullable=False)
    diagnosed_condition = db.Column(db.String(200))
    ayurvedic_remedy = db.Column(db.Text)
    medicine_suggestion = db.Column(db.Text)
    confidence_score = db.Column(db.Float)
    severity_level = db.Column(db.String(20))
    user_feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert diagnosis history to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'condition_id': self.condition_id,
            'symptoms': self.symptoms,
            'diagnosed_condition': self.diagnosed_condition,
            'ayurvedic_remedy': self.ayurvedic_remedy,
            'medicine_suggestion': self.medicine_suggestion,
            'confidence_score': self.confidence_score,
            'severity_level': self.severity_level,
            'user_feedback': self.user_feedback,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<DiagnosisHistory {self.id} - {self.diagnosed_condition}>' 