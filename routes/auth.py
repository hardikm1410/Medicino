"""
Authentication routes for Medicino application.
Handles user registration, login, logout, and profile management.
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from services import UserService, ValidationService
from models import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        # Validate input
        errors = []
        
        if not username:
            errors.append('Username is required')
        elif not ValidationService.validate_username(username)[0]:
            errors.append('Invalid username format')
        
        if not email:
            errors.append('Email is required')
        elif not ValidationService.validate_email(email):
            errors.append('Invalid email format')
        
        if not password:
            errors.append('Password is required')
        elif not ValidationService.validate_password(password)[0]:
            errors.append('Password does not meet requirements')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('auth/register.html')
        
        try:
            # Create user
            user = UserService.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False) == 'on'
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('auth/login.html')
        
        try:
            # Authenticate user
            user = UserService.authenticate_user(username, password)
            
            if user:
                if not user.is_active:
                    flash('Account is deactivated. Please contact support.', 'error')
                    return render_template('auth/login.html')
                
                login_user(user, remember=remember)
                
                # Redirect to intended page or dashboard
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid username or password', 'error')
                
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout endpoint."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management endpoint."""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        phone = request.form.get('phone', '').strip()
        gender = request.form.get('gender', '').strip()
        
        try:
            # Update user profile
            user = UserService.update_user_profile(
                user_id=current_user.id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                gender=gender
            )
            
            if user:
                flash('Profile updated successfully!', 'success')
            else:
                flash('Failed to update profile.', 'error')
                
        except Exception as e:
            flash('An error occurred while updating profile.', 'error')
    
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password endpoint."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate current password
        if not current_user.verify_password(current_password):
            flash('Current password is incorrect', 'error')
            return render_template('auth/change_password.html')
        
        # Validate new password
        if not ValidationService.validate_password(new_password)[0]:
            flash('New password does not meet requirements', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('auth/change_password.html')
        
        try:
            # Update password
            current_user.password = new_password
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            flash('An error occurred while changing password.', 'error')
    
    return render_template('auth/change_password.html')

# API endpoints for authentication
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint for user registration."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    
    # Validate input
    if not all([username, email, password]):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    try:
        user = UserService.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for user login."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    try:
        user = UserService.authenticate_user(username, password)
        
        if user and user.is_active:
            login_user(user)
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict()
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': 'An error occurred during login'}), 500

@auth_bp.route('/api/logout')
@login_required
def api_logout():
    """API endpoint for user logout."""
    logout_user()
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }) 