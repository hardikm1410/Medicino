"""
Tests for Medicino service layer.
Comprehensive testing of business logic and data operations.
"""

import pytest
import tempfile
import os
from datetime import datetime
from unittest.mock import patch, MagicMock

from app_enhanced import create_app
from models import db, User, Medicine, Condition, DiagnosisHistory
from services import (
    UserService, MedicineService, ConditionService, 
    DiagnosisService, ValidationService
)


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.password = 'testpass123'
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def sample_medicine(app):
    """Create a sample medicine for testing."""
    with app.app_context():
        medicine = Medicine(
            name='Paracetamol',
            description='Pain reliever and fever reducer',
            dosage='500-1000mg every 4-6 hours',
            side_effects='Nausea, stomach upset',
            contraindications='Liver disease, alcohol use',
            price=5.99,
            category='Pain Relief'
        )
        db.session.add(medicine)
        db.session.commit()
        return medicine


@pytest.fixture
def sample_condition(app):
    """Create a sample condition for testing."""
    with app.app_context():
        condition = Condition(
            name='Common Cold',
            description='Viral infection of the upper respiratory tract',
            symptoms='runny nose, sore throat, cough, fever',
            ayurvedic_remedy='Tulsi tea, ginger honey',
            modern_treatment='Rest, fluids, over-the-counter medications',
            severity_level='mild',
            category='Respiratory'
        )
        db.session.add(condition)
        db.session.commit()
        return condition


class TestUserService:
    """Test UserService functionality."""
    
    def test_create_user_success(self, app):
        """Test successful user creation."""
        with app.app_context():
            user = UserService.create_user(
                username='newuser',
                email='new@example.com',
                password='password123',
                first_name='New',
                last_name='User'
            )
            
            assert user.username == 'newuser'
            assert user.email == 'new@example.com'
            assert user.first_name == 'New'
            assert user.last_name == 'User'
            assert user.verify_password('password123')
    
    def test_create_user_duplicate_username(self, app, sample_user):
        """Test user creation with duplicate username."""
        with app.app_context():
            with pytest.raises(ValueError, match='Username already exists'):
                UserService.create_user(
                    username='testuser',
                    email='different@example.com',
                    password='password123'
                )
    
    def test_create_user_duplicate_email(self, app, sample_user):
        """Test user creation with duplicate email."""
        with app.app_context():
            with pytest.raises(ValueError, match='Email already exists'):
                UserService.create_user(
                    username='differentuser',
                    email='test@example.com',
                    password='password123'
                )
    
    def test_create_user_short_password(self, app):
        """Test user creation with short password."""
        with app.app_context():
            with pytest.raises(ValueError, match='Password must be at least 6 characters long'):
                UserService.create_user(
                    username='newuser',
                    email='new@example.com',
                    password='123'
                )
    
    def test_authenticate_user_success(self, app, sample_user):
        """Test successful user authentication."""
        with app.app_context():
            user = UserService.authenticate_user('testuser', 'testpass123')
            assert user is not None
            assert user.username == 'testuser'
    
    def test_authenticate_user_invalid_credentials(self, app, sample_user):
        """Test user authentication with invalid credentials."""
        with app.app_context():
            user = UserService.authenticate_user('testuser', 'wrongpassword')
            assert user is None
    
    def test_get_user_by_username(self, app, sample_user):
        """Test getting user by username."""
        with app.app_context():
            user = UserService.get_user_by_username('testuser')
            assert user is not None
            assert user.username == 'testuser'
    
    def test_get_user_by_email(self, app, sample_user):
        """Test getting user by email."""
        with app.app_context():
            user = UserService.get_user_by_email('test@example.com')
            assert user is not None
            assert user.email == 'test@example.com'
    
    def test_update_user_profile(self, app, sample_user):
        """Test updating user profile."""
        with app.app_context():
            user = UserService.update_user_profile(
                user_id=sample_user.id,
                first_name='Updated',
                last_name='Name'
            )
            
            assert user.first_name == 'Updated'
            assert user.last_name == 'Name'


class TestMedicineService:
    """Test MedicineService functionality."""
    
    def test_get_all_medicines(self, app, sample_medicine):
        """Test getting all medicines."""
        with app.app_context():
            medicines = MedicineService.get_all_medicines()
            assert len(medicines) == 1
            assert medicines[0].name == 'Paracetamol'
    
    def test_get_medicine_by_id(self, app, sample_medicine):
        """Test getting medicine by ID."""
        with app.app_context():
            medicine = MedicineService.get_medicine_by_id(sample_medicine.id)
            assert medicine is not None
            assert medicine.name == 'Paracetamol'
    
    def test_get_medicine_by_name(self, app, sample_medicine):
        """Test getting medicine by name."""
        with app.app_context():
            medicine = MedicineService.get_medicine_by_name('Paracetamol')
            assert medicine is not None
            assert medicine.name == 'Paracetamol'
    
    def test_search_medicines(self, app, sample_medicine):
        """Test searching medicines."""
        with app.app_context():
            medicines = MedicineService.search_medicines(query='pain')
            assert len(medicines) == 1
            assert 'pain' in medicines[0].description.lower()
    
    def test_get_medicines_by_category(self, app, sample_medicine):
        """Test getting medicines by category."""
        with app.app_context():
            medicines = MedicineService.get_medicines_by_category('Pain Relief')
            assert len(medicines) == 1
            assert medicines[0].category == 'Pain Relief'
    
    def test_get_medicine_categories(self, app, sample_medicine):
        """Test getting medicine categories."""
        with app.app_context():
            categories = MedicineService.get_medicine_categories()
            assert 'Pain Relief' in categories


class TestConditionService:
    """Test ConditionService functionality."""
    
    def test_get_all_conditions(self, app, sample_condition):
        """Test getting all conditions."""
        with app.app_context():
            conditions = ConditionService.get_all_conditions()
            assert len(conditions) == 1
            assert conditions[0].name == 'Common Cold'
    
    def test_get_condition_by_id(self, app, sample_condition):
        """Test getting condition by ID."""
        with app.app_context():
            condition = ConditionService.get_condition_by_id(sample_condition.id)
            assert condition is not None
            assert condition.name == 'Common Cold'
    
    def test_get_condition_by_name(self, app, sample_condition):
        """Test getting condition by name."""
        with app.app_context():
            condition = ConditionService.get_condition_by_name('Common Cold')
            assert condition is not None
            assert condition.name == 'Common Cold'
    
    def test_search_conditions(self, app, sample_condition):
        """Test searching conditions."""
        with app.app_context():
            conditions = ConditionService.search_conditions(query='cold')
            assert len(conditions) == 1
            assert 'cold' in conditions[0].name.lower()
    
    def test_get_condition_categories(self, app, sample_condition):
        """Test getting condition categories."""
        with app.app_context():
            categories = ConditionService.get_condition_categories()
            assert 'Respiratory' in categories


class TestDiagnosisService:
    """Test DiagnosisService functionality."""
    
    def test_diagnose_symptoms_no_input(self, app):
        """Test diagnosis with no symptoms."""
        with app.app_context():
            result = DiagnosisService.diagnose_symptoms('')
            assert result['disease'] == 'No symptoms provided'
            assert result['confidence'] == 0
    
    def test_diagnose_symptoms_matching_condition(self, app, sample_condition):
        """Test diagnosis with matching symptoms."""
        with app.app_context():
            result = DiagnosisService.diagnose_symptoms('runny nose, sore throat')
            assert 'Common Cold' in result['disease']
            assert result['confidence'] > 0
    
    def test_diagnose_symptoms_no_match(self, app):
        """Test diagnosis with no matching symptoms."""
        with app.app_context():
            result = DiagnosisService.diagnose_symptoms('unknown symptom')
            assert result['disease'] == 'No matching conditions found'
            assert result['confidence'] == 0
    
    def test_save_diagnosis(self, app, sample_user):
        """Test saving diagnosis to history."""
        with app.app_context():
            diagnosis_result = {
                'disease': 'Test Condition',
                'ayurvedic': 'Test remedy',
                'medicine': 'Test medicine',
                'confidence': 75,
                'severity': 'moderate'
            }
            
            diagnosis = DiagnosisService.save_diagnosis(
                user_id=sample_user.id,
                symptoms='test symptoms',
                diagnosis_result=diagnosis_result
            )
            
            assert diagnosis.user_id == sample_user.id
            assert diagnosis.symptoms == 'test symptoms'
            assert diagnosis.diagnosed_condition == 'Test Condition'
    
    def test_get_user_diagnosis_history(self, app, sample_user):
        """Test getting user diagnosis history."""
        with app.app_context():
            # Create a test diagnosis
            diagnosis = DiagnosisHistory(
                user_id=sample_user.id,
                symptoms='test symptoms',
                diagnosed_condition='Test Condition',
                confidence_score=0.75
            )
            db.session.add(diagnosis)
            db.session.commit()
            
            history = DiagnosisService.get_user_diagnosis_history(
                user_id=sample_user.id
            )
            
            assert len(history) == 1
            assert history[0].diagnosed_condition == 'Test Condition'


class TestValidationService:
    """Test ValidationService functionality."""
    
    def test_validate_email_valid(self):
        """Test valid email validation."""
        assert ValidationService.validate_email('test@example.com') == True
        assert ValidationService.validate_email('user.name@domain.co.uk') == True
    
    def test_validate_email_invalid(self):
        """Test invalid email validation."""
        assert ValidationService.validate_email('invalid-email') == False
        assert ValidationService.validate_email('test@') == False
        assert ValidationService.validate_email('@example.com') == False
    
    def test_validate_password_valid(self):
        """Test valid password validation."""
        is_valid, message = ValidationService.validate_password('Password123')
        assert is_valid == True
        assert 'valid' in message.lower()
    
    def test_validate_password_short(self):
        """Test short password validation."""
        is_valid, message = ValidationService.validate_password('123')
        assert is_valid == False
        assert '6 characters' in message
    
    def test_validate_password_no_uppercase(self):
        """Test password without uppercase validation."""
        is_valid, message = ValidationService.validate_password('password123')
        assert is_valid == False
        assert 'uppercase' in message
    
    def test_validate_password_no_lowercase(self):
        """Test password without lowercase validation."""
        is_valid, message = ValidationService.validate_password('PASSWORD123')
        assert is_valid == False
        assert 'lowercase' in message
    
    def test_validate_password_no_number(self):
        """Test password without number validation."""
        is_valid, message = ValidationService.validate_password('Password')
        assert is_valid == False
        assert 'number' in message
    
    def test_validate_username_valid(self):
        """Test valid username validation."""
        is_valid, message = ValidationService.validate_username('testuser')
        assert is_valid == True
        assert 'valid' in message.lower()
    
    def test_validate_username_short(self):
        """Test short username validation."""
        is_valid, message = ValidationService.validate_username('ab')
        assert is_valid == False
        assert '3 characters' in message
    
    def test_validate_username_long(self):
        """Test long username validation."""
        is_valid, message = ValidationService.validate_username('a' * 25)
        assert is_valid == False
        assert '20 characters' in message
    
    def test_validate_username_invalid_chars(self):
        """Test username with invalid characters."""
        is_valid, message = ValidationService.validate_username('test-user')
        assert is_valid == False
        assert 'letters, numbers, and underscores' in message
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        input_text = '<script>alert("xss")</script>Hello & World'
        sanitized = ValidationService.sanitize_input(input_text)
        assert '<script>' not in sanitized
        assert '&' not in sanitized
        assert 'Hello World' in sanitized


if __name__ == '__main__':
    pytest.main([__file__]) 