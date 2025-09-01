"""
Main routes for Medicino application.
Handles web interface pages and user interactions.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from services import MedicineService, ConditionService, DiagnosisService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page - redirects to dashboard if authenticated, otherwise shows landing."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('landing.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard for authenticated users."""
    return render_template('dashboard.html')

@main_bp.route('/app')
@login_required
def main_app():
    """Main application page with diagnosis functionality."""
    return render_template('index.html')

@main_bp.route('/medicines')
@login_required
def medicines():
    """Medicines page."""
    try:
        # Get medicines for display
        medicines_list = MedicineService.get_all_medicines()
        categories = MedicineService.get_medicine_categories()
        
        return render_template('medicines.html', 
                             medicines=medicines_list, 
                             categories=categories)
    except Exception as e:
        flash('Error loading medicines. Please try again.', 'error')
        return render_template('medicines.html', medicines=[], categories=[])

@main_bp.route('/conditions')
@login_required
def conditions():
    """Medical conditions page."""
    try:
        # Get conditions for display
        conditions_list = ConditionService.get_all_conditions()
        categories = ConditionService.get_condition_categories()
        
        return render_template('conditions.html', 
                             conditions=conditions_list, 
                             categories=categories)
    except Exception as e:
        flash('Error loading conditions. Please try again.', 'error')
        return render_template('conditions.html', conditions=[], categories=[])

@main_bp.route('/history')
@login_required
def history():
    """User's diagnosis history page."""
    try:
        # Get user's diagnosis history
        history = DiagnosisService.get_user_diagnosis_history(
            user_id=current_user.id,
            limit=50
        )
        
        return render_template('history.html', history=history)
    except Exception as e:
        flash('Error loading history. Please try again.', 'error')
        return render_template('history.html', history=[])

@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')

@main_bp.route('/privacy')
def privacy():
    """Privacy policy page."""
    return render_template('privacy.html')

@main_bp.route('/terms')
def terms():
    """Terms of service page."""
    return render_template('terms.html')

@main_bp.route('/help')
def help():
    """Help and FAQ page."""
    return render_template('help.html')

@main_bp.route('/search')
@login_required
def search():
    """Search functionality page."""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all')  # all, medicines, conditions
    
    results = {
        'medicines': [],
        'conditions': [],
        'query': query,
        'type': search_type
    }
    
    if query:
        try:
            if search_type in ['all', 'medicines']:
                results['medicines'] = MedicineService.search_medicines(query=query)
            
            if search_type in ['all', 'conditions']:
                results['conditions'] = ConditionService.search_conditions(query=query)
                
        except Exception as e:
            flash('Error performing search. Please try again.', 'error')
    
    return render_template('search.html', results=results)

@main_bp.route('/symptoms')
@login_required
def symptoms():
    """Symptoms reference page."""
    try:
        # Get all conditions to extract symptoms
        conditions = ConditionService.get_all_conditions()
        
        # Extract unique symptoms
        all_symptoms = set()
        for condition in conditions:
            if condition.symptoms:
                symptoms_list = [s.strip().lower() for s in condition.symptoms.split(',')]
                all_symptoms.update(symptoms_list)
        
        # Sort symptoms alphabetically
        symptoms_list = sorted(list(all_symptoms))
        
        return render_template('symptoms.html', symptoms=symptoms_list)
    except Exception as e:
        flash('Error loading symptoms. Please try again.', 'error')
        return render_template('symptoms.html', symptoms=[])

@main_bp.route('/emergency')
def emergency():
    """Emergency information page."""
    return render_template('emergency.html')

@main_bp.route('/disclaimer')
def disclaimer():
    """Medical disclaimer page."""
    return render_template('disclaimer.html')

# Error pages
@main_bp.route('/404')
def not_found():
    """404 error page."""
    return render_template('errors/404.html'), 404

@main_bp.route('/500')
def internal_error():
    """500 error page."""
    return render_template('errors/500.html'), 500

@main_bp.route('/maintenance')
def maintenance():
    """Maintenance page."""
    return render_template('maintenance.html'), 503 