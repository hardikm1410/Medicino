"""
Business logic services for Medicino application.
Separates business logic from controllers for better maintainability.
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from models import db, User, Medicine, SymptomsDatabase, DiagnosisHistory, HealthcareProvider, MedicineSymptomMapping
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
        """Get medicine by name."""
        return Medicine.query.filter_by(name=name).first()
    
    @staticmethod
    def search_medicines(query: str, category: str = None) -> List[Medicine]:
        """Search medicines by name or description."""
        search_query = Medicine.query.filter(Medicine.is_active == True)
        
        if query:
            search_query = search_query.filter(
                db.or_(
                    Medicine.name.ilike(f'%{query}%'),
                    Medicine.description.ilike(f'%{query}%'),
                    Medicine.category.ilike(f'%{query}%')
                )
            )
        
        if category:
            search_query = search_query.filter(Medicine.category.ilike(f'%{category}%'))
        
        return search_query.order_by(Medicine.name).all()
    
    @staticmethod
    def get_medicines_by_category(category: str) -> List[Medicine]:
        """Get medicines by category."""
        return Medicine.query.filter_by(category=category, is_active=True).order_by(Medicine.name).all()
    
    @staticmethod
    def get_medicine_categories() -> List[str]:
        """Get all medicine categories."""
        categories = db.session.query(Medicine.category).filter_by(is_active=True).distinct().all()
        return [cat[0] for cat in categories if cat[0]]
    
    @staticmethod
    def search_medicines_by_symptoms(symptoms_text: str, limit: int = 20) -> Dict:
        """
        Search medicines based on symptoms by matching symptoms to conditions
        and then finding relevant medicines.
        
        Args:
            symptoms_text: Comma-separated symptoms
            limit: Maximum number of medicines to return
            
        Returns:
            Dictionary containing matched medicines and conditions
        """
        if not symptoms_text or not symptoms_text.strip():
            return {
                'medicines': [],
                'conditions': [],
                'message': 'Please provide symptoms to search for medicines.',
                'total_medicines': 0,
                'total_conditions': 0
            }
        
        # Process input symptoms
        input_symptoms = [s.strip().lower() for s in symptoms_text.split(',') if s.strip()]
        
        # Get all conditions from symptoms database
        from sqlalchemy import text
        conditions_query = text("""
            SELECT condition_name, symptoms, medicine_suggestion, severity_level, description
            FROM symptoms_database
        """)
        conditions_result = db.session.execute(conditions_query)
        
        # Find matching conditions
        matched_conditions = []
        all_medicines = set()  # Use set to avoid duplicates
        
        for row in conditions_result:
            condition_name = row[0]
            condition_symptoms = [s.strip().lower() for s in row[1].split(',')]
            medicine_suggestion = row[2]
            severity_level = row[3]
            description = row[4]
            
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
            
            # Include conditions that have at least one matching symptom
            if matches > 0:
                score = matches / len(input_symptoms) if input_symptoms else 0
                
                matched_conditions.append({
                    'condition_name': condition_name,
                    'score': round(score * 100, 1),
                    'matches': matches,
                    'matched_symptoms': list(set(matched_symptoms)),  # Remove duplicates
                    'severity_level': severity_level,
                    'description': description,
                    'medicine_suggestion': medicine_suggestion
                })
                
                # Extract medicine names from medicine_suggestion
                if medicine_suggestion:
                    # Split by common separators and clean up
                    medicine_names = []
                    for part in medicine_suggestion.split(','):
                        part = part.strip()
                        if part:
                            # Remove common prefixes/suffixes
                            part = part.replace('(', '').replace(')', '')
                            medicine_names.append(part)
                    
                    all_medicines.update(medicine_names)
        
        # Sort conditions by score (highest first)
        matched_conditions.sort(key=lambda x: x['score'], reverse=True)
        
        # Search for medicines in the medicines table
        matched_medicines = []
        for medicine_name in list(all_medicines)[:limit]:
            # Search for exact name or similar names
            medicine = MedicineService.search_medicines(medicine_name)
            if medicine:
                matched_medicines.extend(medicine)
        
        # Remove duplicates and limit results
        unique_medicines = []
        seen_ids = set()
        for medicine in matched_medicines:
            if medicine.id not in seen_ids and len(unique_medicines) < limit:
                unique_medicines.append(medicine)
                seen_ids.add(medicine.id)
        
        # Convert to dictionaries
        medicines_data = [medicine.to_dict() for medicine in unique_medicines]
        conditions_data = matched_conditions[:limit]  # Limit conditions too
        
        return {
            'medicines': medicines_data,
            'conditions': conditions_data,
            'message': f'Found {len(medicines_data)} medicines and {len(conditions_data)} conditions for your symptoms.',
            'total_medicines': len(medicines_data),
            'total_conditions': len(conditions_data),
            'search_symptoms': input_symptoms
        }


class SymptomsService:
    """Service class for symptoms database operations."""
    
    @staticmethod
    def get_all_conditions(active_only: bool = True) -> List[SymptomsDatabase]:
        """Get all conditions, optionally filtered by active status."""
        query = SymptomsDatabase.query
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(SymptomsDatabase.condition_name).all()
    
    @staticmethod
    def get_condition_by_id(condition_id: int) -> Optional[SymptomsDatabase]:
        """Get condition by ID."""
        return SymptomsDatabase.query.get(condition_id)
    
    @staticmethod
    def get_condition_by_name(name: str) -> Optional[SymptomsDatabase]:
        """Get condition by name (case-insensitive)."""
        return SymptomsDatabase.query.filter(
            SymptomsDatabase.condition_name.ilike(f'%{name}%')
        ).first()
    
    @staticmethod
    def search_conditions(query: str, category: str = None, body_system: str = None) -> List[SymptomsDatabase]:
        """Search conditions by name, symptoms, or category."""
        search_query = SymptomsDatabase.query.filter(SymptomsDatabase.is_active == True)
        
        if query:
            search_query = search_query.filter(
                db.or_(
                    SymptomsDatabase.condition_name.ilike(f'%{query}%'),
                    SymptomsDatabase.symptoms.ilike(f'%{query}%'),
                    SymptomsDatabase.description.ilike(f'%{query}%')
                )
            )
        
        if category:
            search_query = search_query.filter(
                SymptomsDatabase.category.ilike(f'%{category}%')
            )
        
        if body_system:
            search_query = search_query.filter(
                SymptomsDatabase.body_system.ilike(f'%{body_system}%')
            )
        
        return search_query.order_by(SymptomsDatabase.condition_name).all()
    
    @staticmethod
    def get_condition_categories() -> List[str]:
        """Get all unique condition categories."""
        categories = db.session.query(SymptomsDatabase.category).filter(
            SymptomsDatabase.category.isnot(None),
            SymptomsDatabase.is_active == True
        ).distinct().all()
        return [cat[0] for cat in categories if cat[0]]
    
    @staticmethod
    def get_body_systems() -> List[str]:
        """Get all unique body systems."""
        body_systems = db.session.query(SymptomsDatabase.body_system).filter(
            SymptomsDatabase.body_system.isnot(None),
            SymptomsDatabase.is_active == True
        ).distinct().all()
        return [system[0] for system in body_systems if system[0]]


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
        conditions = SymptomsService.get_all_conditions()
        
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
                    'condition': condition.condition_name,
                    'score': score,
                    'matches': matches,
                    'matched_symptoms': matched_symptoms,
                    'severity': condition.severity_level,
                    'ayurvedic': condition.ayurvedic_remedy,
                    'medicine': condition.medicine_suggestion,
                    'description': condition.description,
                    'precautions': condition.precautions or 'Always seek professional medical advice for an accurate diagnosis.'
                })
                
                if score > best_score:
                    best_score = score
                    best_match = condition
        
        # Sort matches by score (highest first)
        all_matches.sort(key=lambda x: x['score'], reverse=True)
        
        # If we have a very strong match (80% or more symptoms match), show it as primary
        if best_match and best_score >= 0.8:
            return {
                'disease': best_match.condition_name,
                'ayurvedic': best_match.ayurvedic_remedy,
                'medicine': best_match.medicine_suggestion,
                'confidence': round(best_score * 100, 0),
                'severity': best_match.severity_level,
                'description': best_match.description,
                'precautions': best_match.precautions or 'Always seek professional medical advice for an accurate diagnosis.'
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


class HealthcareProviderService:
    """Service class for healthcare provider operations."""
    
    @staticmethod
    def get_all_providers(active_only: bool = True) -> List[HealthcareProvider]:
        """Get all healthcare providers."""
        query = HealthcareProvider.query
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(HealthcareProvider.doctor_name).all()
    
    @staticmethod
    def get_provider_by_id(provider_id: int) -> Optional[HealthcareProvider]:
        """Get healthcare provider by ID."""
        return HealthcareProvider.query.filter_by(id=provider_id, is_active=True).first()
    
    @staticmethod
    def get_provider_by_name(doctor_name: str) -> Optional[HealthcareProvider]:
        """Get healthcare provider by doctor name."""
        return HealthcareProvider.query.filter_by(doctor_name=doctor_name, is_active=True).first()
    
    @staticmethod
    def search_providers(query: str, specialty: str = None, limit: int = 20) -> List[HealthcareProvider]:
        """Search healthcare providers by name, hospital, or specialty."""
        search_query = HealthcareProvider.query.filter_by(is_active=True)
        
        if query:
            search_term = f"%{query}%"
            search_query = search_query.filter(
                db.or_(
                    HealthcareProvider.doctor_name.ilike(search_term),
                    HealthcareProvider.hospital_clinic.ilike(search_term),
                    HealthcareProvider.specialty.ilike(search_term)
                )
            )
        
        if specialty:
            search_query = search_query.filter(HealthcareProvider.specialty.ilike(f"%{specialty}%"))
        
        return search_query.order_by(HealthcareProvider.doctor_name).limit(limit).all()
    
    @staticmethod
    def get_providers_by_specialty(specialty: str) -> List[HealthcareProvider]:
        """Get healthcare providers by specialty."""
        return HealthcareProvider.query.filter_by(
            specialty=specialty, 
            is_active=True
        ).order_by(HealthcareProvider.doctor_name).all()
    
    @staticmethod
    def get_provider_specialties() -> List[str]:
        """Get all available specialties."""
        specialties = db.session.query(HealthcareProvider.specialty)\
            .filter_by(is_active=True)\
            .distinct()\
            .order_by(HealthcareProvider.specialty)\
            .all()
        return [specialty[0] for specialty in specialties]
    
    @staticmethod
    def find_doctors_by_symptoms(symptoms_text: str, limit: int = 10) -> Dict:
        """
        Find relevant doctors based on symptoms by matching symptoms to medical specialties.
        """
        if not symptoms_text or not symptoms_text.strip():
            return {
                'providers': [],
                'message': 'Please provide symptoms to find relevant doctors.',
                'total_providers': 0,
                'search_symptoms': []
            }
        
        input_symptoms = [s.strip().lower() for s in symptoms_text.split(',') if s.strip()]
        
        # Define symptom to specialty mappings
        symptom_specialty_mapping = {
            # General symptoms
            'fever': ['General Physician', 'Pediatrics / Neonatology'],
            'headache': ['General Physician', 'Neurology', 'Neurosurgery'],
            'fatigue': ['General Physician', 'Psychiatry'],
            'pain': ['General Physician', 'Orthopedic Surgery'],
            'nausea': ['General Physician', 'Gastroenterology'],
            'vomiting': ['General Physician', 'Gastroenterology', 'Pediatrics / Neonatology'],
            'dizziness': ['General Physician', 'Cardiology / Cardiothoracic Surgery', 'Neurology'],
            
            # Respiratory symptoms
            'cough': ['General Physician', 'Pediatrics / Neonatology'],
            'sore throat': ['General Physician', 'Pediatrics / Neonatology'],
            'runny nose': ['General Physician', 'Pediatrics / Neonatology'],
            'shortness of breath': ['General Physician', 'Cardiology / Cardiothoracic Surgery', 'Pulmonology'],
            'chest pain': ['General Physician', 'Cardiology / Cardiothoracic Surgery'],
            
            # Digestive symptoms
            'stomach pain': ['General Physician', 'Gastroenterology'],
            'abdominal pain': ['General Physician', 'Gastroenterology'],
            'diarrhea': ['General Physician', 'Gastroenterology', 'Pediatrics / Neonatology'],
            'constipation': ['General Physician', 'Gastroenterology'],
            'heartburn': ['General Physician', 'Gastroenterology'],
            'bloating': ['General Physician', 'Gastroenterology'],
            
            # Mental health symptoms
            'anxiety': ['General Physician', 'Psychiatry'],
            'depression': ['General Physician', 'Psychiatry'],
            'stress': ['General Physician', 'Psychiatry'],
            'insomnia': ['General Physician', 'Psychiatry'],
            'mood swings': ['General Physician', 'Psychiatry'],
            
            # Women's health
            'pregnancy': ['Obstetrics & Gynecology'],
            'menstrual': ['Obstetrics & Gynecology'],
            'gynecological': ['Obstetrics & Gynecology'],
            'breast': ['Obstetrics & Gynecology'],
            
            # Eye symptoms
            'eye pain': ['Ophthalmology'],
            'blurred vision': ['Ophthalmology'],
            'red eyes': ['Ophthalmology'],
            'eye discharge': ['Ophthalmology'],
            
            # Neurological symptoms
            'seizures': ['Neurology', 'Neurosurgery'],
            'numbness': ['Neurology', 'Neurosurgery'],
            'tingling': ['Neurology', 'Neurosurgery'],
            'memory loss': ['Neurology', 'Psychiatry'],
            'confusion': ['Neurology', 'Psychiatry'],
            
            # Cardiovascular symptoms
            'palpitations': ['Cardiology / Cardiothoracic Surgery'],
            'irregular heartbeat': ['Cardiology / Cardiothoracic Surgery'],
            'high blood pressure': ['Cardiology / Cardiothoracic Surgery'],
            'swelling': ['Cardiology / Cardiothoracic Surgery', 'General Physician'],
            
            # Urological symptoms
            'urinary': ['Urology / General Surgery'],
            'bladder': ['Urology / General Surgery'],
            'kidney': ['Urology / General Surgery'],
            'prostate': ['Urology / General Surgery'],
            
            # Orthopedic symptoms
            'joint pain': ['Orthopedic Surgery'],
            'back pain': ['Orthopedic Surgery', 'Neurology'],
            'neck pain': ['Orthopedic Surgery', 'Neurology'],
            'fracture': ['Orthopedic Surgery'],
            'sprain': ['Orthopedic Surgery'],
            
            # Pediatric symptoms
            'child': ['Pediatrics / Neonatology'],
            'baby': ['Pediatrics / Neonatology'],
            'infant': ['Pediatrics / Neonatology'],
            'developmental': ['Pediatrics / Neonatology'],
            
            # Alternative medicine
            'holistic': ['Homeopathy'],
            'natural': ['Homeopathy'],
            'alternative': ['Homeopathy'],
            'ayurvedic': ['Homeopathy']
        }
        
        # Find relevant specialties based on symptoms
        relevant_specialties = set()
        for symptom in input_symptoms:
            for key, specialties in symptom_specialty_mapping.items():
                if key in symptom:
                    relevant_specialties.update(specialties)
        
        # If no specific specialties found, default to General Physician
        if not relevant_specialties:
            relevant_specialties = {'General Physician'}
        
        # Get providers for relevant specialties
        providers = []
        for specialty in list(relevant_specialties)[:5]:  # Limit to top 5 specialties
            specialty_providers = HealthcareProviderService.get_providers_by_specialty(specialty)
            providers.extend(specialty_providers)
        
        # Remove duplicates and limit results
        unique_providers = []
        seen_ids = set()
        for provider in providers:
            if provider.id not in seen_ids and len(unique_providers) < limit:
                unique_providers.append(provider)
                seen_ids.add(provider.id)
        
        providers_data = [provider.to_dict() for provider in unique_providers]
        
        return {
            'providers': providers_data,
            'message': f'Found {len(providers_data)} healthcare providers for your symptoms.',
            'total_providers': len(providers_data),
            'search_symptoms': input_symptoms,
            'relevant_specialties': list(relevant_specialties)
        }
    
    @staticmethod
    def create_provider(doctor_name: str, hospital_clinic: str, hospital_clinic_address: str,
                       hospital_clinic_contact_number: str, specialty: str, **kwargs) -> HealthcareProvider:
        """Create a new healthcare provider."""
        provider = HealthcareProvider(
            doctor_name=doctor_name,
            hospital_clinic=hospital_clinic,
            hospital_clinic_address=hospital_clinic_address,
            hospital_clinic_contact_number=hospital_clinic_contact_number,
            specialty=specialty,
            **kwargs
        )
        
        db.session.add(provider)
        db.session.commit()
        
        return provider
    
    @staticmethod
    def update_provider(provider_id: int, **kwargs) -> Optional[HealthcareProvider]:
        """Update healthcare provider information."""
        provider = HealthcareProviderService.get_provider_by_id(provider_id)
        
        if not provider:
            return None
        
        for key, value in kwargs.items():
            if hasattr(provider, key):
                setattr(provider, key, value)
        
        db.session.commit()
        return provider
    
    @staticmethod
    def deactivate_provider(provider_id: int) -> bool:
        """Deactivate a healthcare provider."""
        provider = HealthcareProviderService.get_provider_by_id(provider_id)
        
        if not provider:
            return False
        
        provider.is_active = False
        db.session.commit()
        
        return True 