"""
API routes for Medicino application.
RESTful API endpoints for diagnosis, medicines, and user data.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from functools import wraps
import logging
from datetime import datetime

from services import (
    DiagnosisService, MedicineService, SymptomsService, 
    UserService, ValidationService, HealthcareProviderService
)
from models import db

api_bp = Blueprint('api', __name__)

def api_error_response(message, status_code=400):
    """Helper function to create consistent API error responses."""
    return jsonify({
        'success': False,
        'error': message
    }), status_code

def api_success_response(data=None, message="Success", status_code=200):
    """Helper function to create consistent API success responses."""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def validate_json_request(f):
    """Decorator to validate JSON request data."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return api_error_response("Content-Type must be application/json", 400)
        return f(*args, **kwargs)
    return decorated_function

# Diagnosis API endpoints
@api_bp.route('/diagnose', methods=['POST'])
@login_required
@validate_json_request
def diagnose():
    """Diagnose symptoms API endpoint."""
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return api_error_response("Symptoms are required", 400)
        
        symptoms = data['symptoms'].strip()
        if not symptoms:
            return api_error_response("Symptoms cannot be empty", 400)
        
        # Sanitize input
        symptoms = ValidationService.sanitize_input(symptoms)
        
        # Perform diagnosis
        diagnosis_result = DiagnosisService.diagnose_symptoms(symptoms)
        
        # Save to history
        diagnosis_record = DiagnosisService.save_diagnosis(
            user_id=current_user.id,
            symptoms=symptoms,
            diagnosis_result=diagnosis_result
        )
        
        # Add diagnosis ID to response
        diagnosis_result['diagnosis_id'] = diagnosis_record.id
        
        return api_success_response(
            data=diagnosis_result,
            message="Diagnosis completed successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Diagnosis error: {str(e)}")
        return api_error_response("An error occurred during diagnosis", 500)

@api_bp.route('/diagnose/history', methods=['GET'])
@login_required
def get_diagnosis_history():
    """Get user's diagnosis history."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        # Get diagnosis history
        history = DiagnosisService.get_user_diagnosis_history(
            user_id=current_user.id,
            limit=per_page
        )
        
        # Convert to list of dictionaries
        history_data = [record.to_dict() for record in history]
        
        return api_success_response(
            data={
                'history': history_data,
                'page': page,
                'per_page': per_page,
                'total': len(history_data)
            },
            message="Diagnosis history retrieved successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving diagnosis history: {str(e)}")
        return api_error_response("An error occurred while retrieving history", 500)

@api_bp.route('/diagnose/<int:diagnosis_id>/feedback', methods=['POST'])
@login_required
@validate_json_request
def update_diagnosis_feedback(diagnosis_id):
    """Update diagnosis with user feedback."""
    try:
        data = request.get_json()
        
        feedback = data.get('feedback', '').strip()
        is_accurate = data.get('is_accurate')
        
        if not feedback:
            return api_error_response("Feedback is required", 400)
        
        # Sanitize feedback
        feedback = ValidationService.sanitize_input(feedback)
        
        # Update diagnosis
        diagnosis = DiagnosisService.update_diagnosis_feedback(
            diagnosis_id=diagnosis_id,
            user_id=current_user.id,
            feedback=feedback,
            is_accurate=is_accurate
        )
        
        if not diagnosis:
            return api_error_response("Diagnosis not found or access denied", 404)
        
        return api_success_response(
            data=diagnosis.to_dict(),
            message="Feedback updated successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error updating diagnosis feedback: {str(e)}")
        return api_error_response("An error occurred while updating feedback", 500)

# Medicine API endpoints
@api_bp.route('/medicines', methods=['GET'])
def get_medicines():
    """Get all medicines with optional filtering."""
    try:
        # Get query parameters
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        # Get medicines based on filters
        if search or category:
            medicines = MedicineService.search_medicines(
                query=search,
                category=category
            )
        else:
            medicines = MedicineService.get_all_medicines()
        
        # Convert to list of dictionaries
        medicines_data = [medicine.to_dict() for medicine in medicines]
        
        return api_success_response(
            data={
                'medicines': medicines_data,
                'page': page,
                'per_page': per_page,
                'total': len(medicines_data)
            },
            message="Medicines retrieved successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving medicines: {str(e)}")
        return api_error_response("An error occurred while retrieving medicines", 500)

@api_bp.route('/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
    """Get specific medicine by ID."""
    try:
        medicine = MedicineService.get_medicine_by_id(medicine_id)
        
        if not medicine:
            return api_error_response("Medicine not found", 404)
        
        return api_success_response(
            data=medicine.to_dict(),
            message="Medicine retrieved successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving medicine: {str(e)}")
        return api_error_response("An error occurred while retrieving medicine", 500)

@api_bp.route('/medicines/search', methods=['GET'])
def search_medicines():
    """Search medicines by name."""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return api_error_response("Search query is required", 400)
        
        medicines = MedicineService.search_medicines(query=query)
        medicines_data = [medicine.to_dict() for medicine in medicines]
        
        return api_success_response(
            data=medicines_data,
            message=f"Found {len(medicines_data)} medicines"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error searching medicines: {str(e)}")
        return api_error_response("An error occurred while searching medicines", 500)

@api_bp.route('/medicines/search-by-symptoms', methods=['POST'])
@validate_json_request
def search_medicines_by_symptoms():
    """Search medicines based on symptoms."""
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return api_error_response("Symptoms are required", 400)
        
        symptoms = data['symptoms'].strip()
        if not symptoms:
            return api_error_response("Symptoms cannot be empty", 400)
        
        # Optional parameters
        limit = data.get('limit', 20)
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            limit = 20
        
        # Sanitize input
        symptoms = ValidationService.sanitize_input(symptoms)
        
        # Search medicines by symptoms
        result = MedicineService.search_medicines_by_symptoms(symptoms, limit=limit)
        
        return api_success_response(
            data=result,
            message=result['message']
        )
        
    except Exception as e:
        current_app.logger.error(f"Error searching medicines by symptoms: {str(e)}")
        return api_error_response("An error occurred while searching medicines by symptoms", 500)

@api_bp.route('/medicines/search-by-symptoms', methods=['GET'])
def search_medicines_by_symptoms_get():
    """Search medicines based on symptoms (GET method for easier testing)."""
    try:
        symptoms = request.args.get('symptoms', '').strip()
        
        if not symptoms:
            return api_error_response("Symptoms parameter is required", 400)
        
        # Optional parameters
        limit = request.args.get('limit', 20, type=int)
        if limit < 1 or limit > 100:
            limit = 20
        
        # Sanitize input
        symptoms = ValidationService.sanitize_input(symptoms)
        
        # Search medicines by symptoms
        result = MedicineService.search_medicines_by_symptoms(symptoms, limit=limit)
        
        return api_success_response(
            data=result,
            message=result['message']
        )
        
    except Exception as e:
        current_app.logger.error(f"Error searching medicines by symptoms: {str(e)}")
        return api_error_response("An error occurred while searching medicines by symptoms", 500)

@api_bp.route('/medicines/categories', methods=['GET'])
def get_medicine_categories():
    """Get all medicine categories."""
    try:
        categories = MedicineService.get_medicine_categories()
        
        return api_success_response(
            data=categories,
            message="Medicine categories retrieved successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving medicine categories: {str(e)}")
        return api_error_response("An error occurred while retrieving categories", 500)

# Condition API endpoints
@api_bp.route('/conditions', methods=['GET'])
def get_conditions():
    """Get all conditions with optional filtering."""
    try:
        # Get query parameters
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        # Get conditions based on filters
        if search or category:
            conditions = SymptomsService.search_conditions(
                query=search,
                category=category
            )
        else:
            conditions = SymptomsService.get_all_conditions()
        
        # Convert to list of dictionaries
        conditions_data = [condition.to_dict() for condition in conditions]
        
        return api_success_response(
            data={
                'conditions': conditions_data,
                'page': page,
                'per_page': per_page,
                'total': len(conditions_data)
            },
            message="Conditions retrieved successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving conditions: {str(e)}")
        return api_error_response("An error occurred while retrieving conditions", 500)

@api_bp.route('/conditions/<int:condition_id>', methods=['GET'])
def get_condition(condition_id):
    """Get specific condition by ID."""
    try:
        condition = SymptomsService.get_condition_by_id(condition_id)
        
        if not condition:
            return api_error_response("Condition not found", 404)
        
        return api_success_response(
            data=condition.to_dict(),
            message="Condition retrieved successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving condition: {str(e)}")
        return api_error_response("An error occurred while retrieving condition", 500)

@api_bp.route('/conditions/categories', methods=['GET'])
def get_condition_categories():
    """Get all condition categories."""
    try:
        categories = SymptomsService.get_condition_categories()
        
        return api_success_response(
            data=categories,
            message="Condition categories retrieved successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving condition categories: {str(e)}")
        return api_error_response("An error occurred while retrieving categories", 500)

# User API endpoints
@api_bp.route('/user/profile', methods=['GET'])
@login_required
def get_user_profile():
    """Get current user's profile."""
    try:
        return api_success_response(
            data=current_user.to_dict(),
            message="User profile retrieved successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving user profile: {str(e)}")
        return api_error_response("An error occurred while retrieving profile", 500)

@api_bp.route('/user/profile', methods=['PUT'])
@login_required
@validate_json_request
def update_user_profile():
    """Update current user's profile."""
    try:
        data = request.get_json()
        
        # Extract allowed fields
        allowed_fields = ['first_name', 'last_name', 'phone', 'gender']
        update_data = {k: v.strip() for k, v in data.items() if k in allowed_fields and v}
        
        if not update_data:
            return api_error_response("No valid fields to update", 400)
        
        # Update user profile
        user = UserService.update_user_profile(
            user_id=current_user.id,
            **update_data
        )
        
        if not user:
            return api_error_response("Failed to update profile", 500)
        
        return api_success_response(
            data=user.to_dict(),
            message="Profile updated successfully"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error updating user profile: {str(e)}")
        return api_error_response("An error occurred while updating profile", 500)

# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Basic health check
        db.session.execute('SELECT 1')
        
        return api_success_response(
            data={
                'status': 'healthy',
                'database': 'connected',
                'timestamp': str(datetime.utcnow())
            },
            message="Service is healthy"
        )
        
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return api_error_response("Service is unhealthy", 503)

# API documentation endpoint
@api_bp.route('/docs', methods=['GET'])
def api_docs():
    """API documentation endpoint."""
    docs = {
        'version': '1.0.0',
        'endpoints': {
            'diagnosis': {
                'POST /api/diagnose': 'Diagnose symptoms and get treatment recommendations',
                'GET /api/diagnose/history': 'Get user diagnosis history',
                'POST /api/diagnose/<id>/feedback': 'Update diagnosis feedback'
            },
            'medicines': {
                'GET /api/medicines': 'Get all medicines',
                'GET /api/medicines/<id>': 'Get specific medicine',
                'GET /api/medicines/search': 'Search medicines',
                'POST /api/medicines/search-by-symptoms': 'Search medicines by symptoms',
                'GET /api/medicines/search-by-symptoms': 'Search medicines by symptoms (GET)',
                'GET /api/medicines/categories': 'Get medicine categories'
            },
            'conditions': {
                'GET /api/conditions': 'Get all conditions',
                'GET /api/conditions/<id>': 'Get specific condition',
                'GET /api/conditions/categories': 'Get condition categories'
            },
            'healthcare_providers': {
                'GET /api/healthcare-providers': 'Get all healthcare providers',
                'GET /api/healthcare-providers/<id>': 'Get specific healthcare provider',
                'GET /api/healthcare-providers/search': 'Search healthcare providers',
                'POST /api/healthcare-providers/search-by-symptoms': 'Find doctors by symptoms',
                'GET /api/healthcare-providers/search-by-symptoms': 'Find doctors by symptoms (GET)',
                'GET /api/healthcare-providers/specialties': 'Get available specialties'
            },
            'user': {
                'GET /api/user/profile': 'Get user profile',
                'PUT /api/user/profile': 'Update user profile'
            },
            'system': {
                'GET /api/health': 'Health check',
                'GET /api/docs': 'API documentation'
            }
        }
    }
    
    return api_success_response(data=docs, message="API Documentation")

# Healthcare Providers API endpoints
@api_bp.route('/healthcare-providers', methods=['GET'])
def get_healthcare_providers():
    """Get all healthcare providers."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        specialty = request.args.get('specialty')
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        # Get providers
        if specialty:
            providers = HealthcareProviderService.get_providers_by_specialty(specialty)
        else:
            providers = HealthcareProviderService.get_all_providers()
        
        # Apply pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_providers = providers[start_idx:end_idx]
        
        providers_data = [provider.to_dict() for provider in paginated_providers]
        
        return api_success_response(
            data={
                'providers': providers_data,
                'total': len(providers),
                'page': page,
                'per_page': per_page,
                'total_pages': (len(providers) + per_page - 1) // per_page
            },
            message=f"Found {len(providers_data)} healthcare providers"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error getting healthcare providers: {str(e)}")
        return api_error_response("An error occurred while fetching healthcare providers", 500)

@api_bp.route('/healthcare-providers/<int:provider_id>', methods=['GET'])
def get_healthcare_provider(provider_id):
    """Get specific healthcare provider by ID."""
    try:
        provider = HealthcareProviderService.get_provider_by_id(provider_id)
        
        if not provider:
            return api_error_response("Healthcare provider not found", 404)
        
        return api_success_response(
            data=provider.to_dict(),
            message="Healthcare provider found"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error getting healthcare provider {provider_id}: {str(e)}")
        return api_error_response("An error occurred while fetching healthcare provider", 500)

@api_bp.route('/healthcare-providers/search', methods=['GET'])
def search_healthcare_providers():
    """Search healthcare providers by name, hospital, or specialty."""
    try:
        query = request.args.get('query', '').strip()
        specialty = request.args.get('specialty', '').strip()
        limit = request.args.get('limit', 20, type=int)
        
        if limit < 1 or limit > 100:
            limit = 20
        
        if not query and not specialty:
            return api_error_response("Query or specialty parameter is required", 400)
        
        # Sanitize inputs
        if query:
            query = ValidationService.sanitize_input(query)
        if specialty:
            specialty = ValidationService.sanitize_input(specialty)
        
        # Search providers
        providers = HealthcareProviderService.search_providers(
            query=query if query else None,
            specialty=specialty if specialty else None,
            limit=limit
        )
        
        providers_data = [provider.to_dict() for provider in providers]
        
        return api_success_response(
            data=providers_data,
            message=f"Found {len(providers_data)} healthcare providers"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error searching healthcare providers: {str(e)}")
        return api_error_response("An error occurred while searching healthcare providers", 500)

@api_bp.route('/healthcare-providers/search-by-symptoms', methods=['POST'])
@validate_json_request
def find_doctors_by_symptoms():
    """Find relevant doctors based on symptoms."""
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return api_error_response("Symptoms are required", 400)
        
        symptoms = data['symptoms'].strip()
        if not symptoms:
            return api_error_response("Symptoms cannot be empty", 400)
        
        # Optional parameters
        limit = data.get('limit', 10)
        if limit < 1 or limit > 50:
            limit = 10
        
        # Sanitize input
        symptoms = ValidationService.sanitize_input(symptoms)
        
        # Find doctors by symptoms
        result = HealthcareProviderService.find_doctors_by_symptoms(symptoms, limit=limit)
        
        return api_success_response(
            data=result,
            message=result['message']
        )
        
    except Exception as e:
        current_app.logger.error(f"Error finding doctors by symptoms: {str(e)}")
        return api_error_response("An error occurred while finding doctors", 500)

@api_bp.route('/healthcare-providers/search-by-symptoms', methods=['GET'])
def find_doctors_by_symptoms_get():
    """Find relevant doctors based on symptoms (GET method for easier testing)."""
    try:
        symptoms = request.args.get('symptoms', '').strip()
        
        if not symptoms:
            return api_error_response("Symptoms parameter is required", 400)
        
        # Optional parameters
        limit = request.args.get('limit', 10, type=int)
        if limit < 1 or limit > 50:
            limit = 10
        
        # Sanitize input
        symptoms = ValidationService.sanitize_input(symptoms)
        
        # Find doctors by symptoms
        result = HealthcareProviderService.find_doctors_by_symptoms(symptoms, limit=limit)
        
        return api_success_response(
            data=result,
            message=result['message']
        )
        
    except Exception as e:
        current_app.logger.error(f"Error finding doctors by symptoms: {str(e)}")
        return api_error_response("An error occurred while finding doctors", 500)

@api_bp.route('/healthcare-providers/specialties', methods=['GET'])
def get_healthcare_provider_specialties():
    """Get all available healthcare provider specialties."""
    try:
        specialties = HealthcareProviderService.get_provider_specialties()
        
        return api_success_response(
            data=specialties,
            message=f"Found {len(specialties)} specialties"
        )
        
    except Exception as e:
        current_app.logger.error(f"Error getting healthcare provider specialties: {str(e)}")
        return api_error_response("An error occurred while fetching specialties", 500) 