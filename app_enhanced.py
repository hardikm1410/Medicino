"""
Enhanced Medicino Web Application
A comprehensive medical assistant with improved architecture, security, and features.
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session, abort
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

# Import our modules
from config import config
from models import db, User, Medicine, Condition, DiagnosisHistory
from services import UserService, MedicineService, ConditionService, DiagnosisService, ValidationService

# Initialize Flask extensions
login_manager = LoginManager()

def create_app(config_name='default'):
    """Application factory pattern for better testing and configuration."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Setup CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.api import api_bp
    from routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)
    
    # Error handlers
    register_error_handlers(app)
    
    # Request handlers
    register_request_handlers(app)
    
    return app

def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Resource not found', 'message': 'The requested resource was not found'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': error.name, 'message': error.description}), error.code
        return render_template('errors/generic.html', error=error), error.code

def register_request_handlers(app):
    """Register request handlers for the application."""
    
    @app.before_request
    def before_request():
        """Handle pre-request tasks."""
        # Log request information
        if not app.debug:
            app.logger.info(f'{request.method} {request.path} - {request.remote_addr}')
        
        # Check for maintenance mode
        if app.config.get('MAINTENANCE_MODE', False) and request.path != '/maintenance':
            return render_template('maintenance.html'), 503
    
    @app.after_request
    def after_request(response):
        """Handle post-request tasks."""
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Add CORS headers
        if 'Origin' in request.headers:
            response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        
        return response

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    return UserService.get_user_by_id(int(user_id))

# Create the application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# CLI commands
@app.cli.command('init-db')
def init_db_command():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

@app.cli.command('create-admin')
def create_admin_command():
    """Create an admin user."""
    username = input('Enter admin username: ')
    email = input('Enter admin email: ')
    password = input('Enter admin password: ')
    
    try:
        user = UserService.create_user(username, email, password, is_admin=True)
        print(f'Admin user {user.username} created successfully.')
    except ValueError as e:
        print(f'Error creating admin user: {e}')

@app.cli.command('seed-data')
def seed_data_command():
    """Seed the database with initial data."""
    from database_setup import seed_database
    seed_database()
    print('Database seeded with initial data.')

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    print("🚀 Starting Enhanced Medicino Web Portal...")
    print(f"📊 Environment: {os.getenv('FLASK_CONFIG', 'development')}")
    print(f"🔗 Access the application at: http://localhost:5000")
    print(f"📝 API Documentation: http://localhost:5000/api/docs")
    
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    ) 