"""
Business logic services for Medicino application.
Separates business logic from controllers for better maintainability.
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from models import db, User, Medicine, Condition, DiagnosisHistory
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    def create_user(username: str, email: str, password: str, **kwargs) -> User:
        """Create a new user."""
        # Validate input
        if not username or not email or not password:
            raise ValueError("Username, email, and password are required")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Check if user already exists
        if UserService.get_user_by_username(username):
            raise ValueError("Username already exists")
        
        if UserService.get_user_by_email(email):
            raise ValueError("Email already exists")
        
        # Create user
        user = User(
            username=username.lower(),
            email=email.lower(),
            **kwargs
        )
        user.password = password
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username."""
        return User.query.filter_by(username=username.lower()).first()
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email."""
        return User.query.filter_by(email=email.lower()).first()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        user = UserService.get_user_by_username(username)
        if user and user.verify_password(password):
            return user
        return None
    
    @staticmethod
    def update_user_profile(user_id: int, **kwargs) -> Optional[User]:
        """Update user profile information."""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None
        
        # Update allowed fields
        allowed_fields = ['first_name', 'last_name', 'phone', 'date_of_birth', 'gender']
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return user


class MedicineService:
    """Service class for medicine-related operations."""
    
    @staticmethod
    def get_all_medicines(active_only: bool = True) -> List[Medicine]:
        """Get all medicines, optionally filtered by active status."""
        query = Medicine.query
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(Medicine.name).all()
    
    @staticmethod
    def get_medicine_by_id(medicine_id: int) -> Optional[Medicine]:
        """Get medicine by ID."""
        return Medicine.query.get(medicine_id)
    
    @staticmethod
    def get_medicine_by_name(name: str) -> Optional[Medicine]:
        """Get medicine by name (case-insensitive)."""
        return Medicine.query.filter(
            Medicine.name.ilike(f'%{name}%')
        ).first()
    
    @staticmethod
    def search_medicines(query: str, category: str = None) -> List[Medicine]:
        """Search medicines by name or category."""
        search_query = Medicine.query.filter(Medicine.is_active == True)
        
        if query:
            search_query = search_query.filter(
                Medicine.name.ilike(f'%{query}%')
            )
        
        if category:
            search_query = search_query.filter(
                Medicine.category.ilike(f'%{category}%')
            )
        
        return search_query.order_by(Medicine.name).all()
    
    @staticmethod
    def get_medicines_by_category(category: str) -> List[Medicine]:
        """Get medicines by category."""
        return Medicine.query.filter(
            Medicine.category.ilike(f'%{category}%'),
            Medicine.is_active == True
        ).order_by(Medicine.name).all()
    
    @staticmethod
    def get_medicine_categories() -> List[str]:
        """Get all unique medicine categories."""
        categories = db.session.query(Medicine.category).filter(
            Medicine.category.isnot(None),
            Medicine.is_active == True
        ).distinct().all()
        return [cat[0] for cat in categories if cat[0]]


class ConditionService:
    """Service class for condition-related operations."""
    
    @staticmethod
    def get_all_conditions(active_only: bool = True) -> List[Condition]:
        """Get all conditions, optionally filtered by active status."""
        query = Condition.query
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(Condition.name).all()
    
    @staticmethod
    def get_condition_by_id(condition_id: int) -> Optional[Condition]:
        """Get condition by ID."""
        return Condition.query.get(condition_id)
    
    @staticmethod
    def get_condition_by_name(name: str) -> Optional[Condition]:
        """Get condition by name (case-insensitive)."""
        return Condition.query.filter(
            Condition.name.ilike(f'%{name}%')
        ).first()
    
    @staticmethod
    def search_conditions(query: str, category: str = None) -> List[Condition]:
        """Search conditions by name, symptoms, or category."""
        search_query = Condition.query.filter(Condition.is_active == True)
        
        if query:
            search_query = search_query.filter(
                db.or_(
                    Condition.name.ilike(f'%{query}%'),
                    Condition.symptoms.ilike(f'%{query}%'),
                    Condition.description.ilike(f'%{query}%')
                )
            )
        
        if category:
            search_query = search_query.filter(
                Condition.category.ilike(f'%{category}%')
            )
        
        return search_query.order_by(Condition.name).all()
    
    @staticmethod
    def get_condition_categories() -> List[str]:
        """Get all unique condition categories."""
        categories = db.session.query(Condition.category).filter(
            Condition.category.isnot(None),
            Condition.is_active == True
        ).distinct().all()
        return [cat[0] for cat in categories if cat[0]]


class DiagnosisService:
    """Service class for diagnosis-related operations."""
    
    @staticmethod
    def diagnose_symptoms(symptoms_text: str) -> Dict:
        """Enhanced symptom diagnosis logic that returns all possible diseases for minimal symptoms."""
        if not symptoms_text or not symptoms_text.strip():
            return {
                'disease': 'No symptoms provided',
                'ayurvedic': 'Please enter your symptoms to get a diagnosis.',
                'medicine': 'Please enter your symptoms to get medicine suggestions.',
                'confidence': 0,
                'severity': 'unknown',
                'description': 'Please describe your symptoms in simple terms like: fever, headache, cough, stomach pain, etc.',
                'precautions': 'Always seek professional medical advice for an accurate diagnosis.'
            }
        
        # Process input symptoms
        input_symptoms = [s.strip().lower() for s in symptoms_text.split(',') if s.strip()]
        
        # Get all conditions
        conditions = ConditionService.get_all_conditions()
        
        # Find all conditions that match ANY of the input symptoms
        all_matches = []
        best_match = None
        best_score = 0
        
        for condition in conditions:
            condition_symptoms = [s.strip().lower() for s in condition.symptoms.split(',')]
            
            # Count how many input symptoms match condition symptoms
            matches = 0
            matched_symptoms = []
            
            for input_symptom in input_symptoms:
                for condition_symptom in condition_symptoms:
                    # Simple contains check
                    if input_symptom in condition_symptom or condition_symptom in input_symptom:
                        matches += 1
                        matched_symptoms.append(condition_symptom)
                        break
            
            # Calculate score: percentage of input symptoms that matched
            if input_symptoms:
                score = matches / len(input_symptoms)
            else:
                score = 0
            
            # Include ALL conditions that have at least one matching symptom
            if matches > 0:
                all_matches.append({
                    'condition': condition.name,
                    'score': score,
                    'matches': matches,
                    'matched_symptoms': matched_symptoms,
                    'severity': condition.severity_level,
                    'ayurvedic': condition.ayurvedic_remedy,
                    'medicine': condition.modern_treatment,
                    'description': condition.description,
                    'precautions': 'Always seek professional medical advice for an accurate diagnosis.'
                })
                
                if score > best_score:
                    best_score = score
                    best_match = condition
        
        # Sort matches by score (highest first)
        all_matches.sort(key=lambda x: x['score'], reverse=True)
        
        # If we have a very strong match (80% or more symptoms match), show it as primary
        if best_match and best_score >= 0.8:
            return {
                'disease': best_match.name,
                'ayurvedic': best_match.ayurvedic_remedy,
                'medicine': best_match.modern_treatment,
                'confidence': round(best_score * 100, 0),
                'severity': best_match.severity_level,
                'description': best_match.description,
                'precautions': 'Always seek professional medical advice for an accurate diagnosis.'
            }
        else:
            # Return ALL possible conditions that match the symptoms
            if all_matches:
                # Create a comprehensive list of all matching conditions
                condition_list = []
                for match in all_matches:
                    severity_emoji = {
                        'mild': '🟢',
                        'moderate': '🟡', 
                        'severe': '🔴',
                        'unknown': '❓'
                    }.get(match['severity'], '❓')
                    
                    confidence_text = f" ({round(match['score'] * 100, 0)}% match)"
                    condition_list.append(f"{severity_emoji} {match['condition']}{confidence_text}")
                
                # Limit to top 10 to avoid overwhelming the user
                top_conditions = condition_list[:10]
                condition_text = "\n• " + "\n• ".join(top_conditions)
                
                # If there are more than 10 matches, add a note
                if len(all_matches) > 10:
                    condition_text += f"\n\n... and {len(all_matches) - 10} more possible conditions"
                
                return {
                    'disease': f'Found {len(all_matches)} possible conditions',
                    'ayurvedic': 'Please consult an Ayurvedic practitioner for personalized treatment.',
                    'medicine': 'Please consult a healthcare professional for proper diagnosis.',
                    'confidence': round(best_score * 100, 0) if best_score > 0 else 0,
                    'severity': 'unknown',
                    'description': f'Your symptoms could indicate these conditions:\n{condition_text}\n\nAdd more symptoms for more accurate results.',
                    'precautions': 'Always seek professional medical advice for an accurate diagnosis. This is not a substitute for medical consultation.'
                }
            else:
                return {
                    'disease': 'No matching conditions found',
                    'ayurvedic': 'Please consult an Ayurvedic practitioner for personalized treatment.',
                    'medicine': 'Please consult a healthcare professional for proper diagnosis.',
                    'confidence': 0,
                    'severity': 'unknown',
                    'description': 'Try describing your symptoms in simple terms like: fever, headache, cough, stomach pain, etc.',
                    'precautions': 'Always seek professional medical advice for an accurate diagnosis.'
                }
    
    @staticmethod
    def save_diagnosis(user_id: int, symptoms: str, diagnosis_result: Dict) -> DiagnosisHistory:
        """Save diagnosis to history."""
        diagnosis = DiagnosisHistory(
            user_id=user_id,
            symptoms=symptoms,
            diagnosed_condition=diagnosis_result.get('disease'),
            ayurvedic_remedy=diagnosis_result.get('ayurvedic'),
            medicine_suggestion=diagnosis_result.get('medicine'),
            confidence_score=diagnosis_result.get('confidence', 0) / 100,  # Convert percentage to decimal
            severity_level=diagnosis_result.get('severity', 'unknown')
        )
        
        db.session.add(diagnosis)
        db.session.commit()
        
        return diagnosis
    
    @staticmethod
    def get_user_diagnosis_history(user_id: int, limit: int = 50) -> List[DiagnosisHistory]:
        """Get diagnosis history for a user."""
        return DiagnosisHistory.query.filter_by(user_id=user_id)\
            .order_by(DiagnosisHistory.created_at.desc())\
            .limit(limit).all()
    
    @staticmethod
    def update_diagnosis_feedback(diagnosis_id: int, user_id: int, feedback: str, is_accurate: bool = None) -> Optional[DiagnosisHistory]:
        """Update diagnosis with user feedback."""
        diagnosis = DiagnosisHistory.query.filter_by(
            id=diagnosis_id, 
            user_id=user_id
        ).first()
        
        if not diagnosis:
            return None
        
        diagnosis.user_feedback = feedback
        if is_accurate is not None:
            diagnosis.is_accurate = is_accurate
        
        db.session.commit()
        return diagnosis


class ValidationService:
    """Service class for input validation."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password strength."""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        return True, "Password is valid"
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate username format."""
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 20:
            return False, "Username must be no more than 20 characters long"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, "Username is valid"
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS."""
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&']
        for char in dangerous_chars:
            text = text.replace(char, '')
        return text.strip() 