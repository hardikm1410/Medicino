from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re
import os
from datetime import datetime
from dotenv import load_dotenv # <-- Add this import

load_dotenv() # <-- Add this line to load variables for local testing

# ... other imports

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION (Updated) ---
# Read secrets from environment variables
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
mongo_uri = os.getenv('MONGO_URI')

# --- DATABASE SETUP (Updated) ---
DATABASE = 'medicino.db'
client = MongoClient(mongo_uri)
db = client['medicino_db']
users_collection = db['users']



# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Configuration


# Apply CORS to the entire application to allow cross-origin requests from your frontend.

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['email'])
    return None

# Custom handler for unauthorized access, returns JSON instead of redirecting
@login_manager.unauthorized_handler
def unauthorized_callback():
    return jsonify({'error': 'Unauthorized', 'message': 'Please log in to access this resource'}), 401

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create database tables if they don't exist."""
    print("Checking for database tables...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create medicines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            dosage TEXT,
            side_effects TEXT,
            contraindications TEXT,
            price REAL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create diagnosis history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symptoms TEXT NOT NULL,
            diagnosed_condition TEXT,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            confidence_score REAL,
            user_feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create symptoms database table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS symptoms_database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_name TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            severity_level TEXT,
            description TEXT,
            precautions TEXT
        )
    ''')

    # Create healthcare providers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS healthcare_providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_name TEXT NOT NULL,
            hospital_clinic TEXT NOT NULL,
            hospital_clinic_address TEXT NOT NULL,
            hospital_clinic_contact_number TEXT NOT NULL,
            specialty TEXT NOT NULL,
            experience_years INTEGER,
            consultation_fee REAL,
            availability TEXT,
            languages_spoken TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database tables are ready!")

# Routes
@app.route('/')
def home():
    return 'Welcome to the Medicino Backend API!'

@app.route('/login', methods=['POST'])
def login():
    # Placeholder for actual login logic
    # In a real app, you would validate credentials here
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        # Create a User object and log them in
        user_obj = User(user['id'], user['username'], user['email'])
        login_user(user_obj)
        return jsonify({'message': 'Login successful', 'username': user['username']}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


# Other routes from your original app.py can be added here
@app.route('/api/diagnosis', methods=['POST'])
@login_required
def get_diagnosis_api():
    # Your diagnosis logic here
    # Placeholder response
    return jsonify({'message': 'Diagnosis API endpoint placeholder'})

@app.route('/api/medicine_info/<medicine_name>')
@login_required
def get_medicine_info_api(medicine_name):
    # Your medicine info logic here
    # Placeholder response
    return jsonify({'message': 'Medicine info API endpoint placeholder'})

@app.route('/api/medicines')
@login_required
def list_medicines_api():
    # Your list medicines logic here
    # Placeholder response
    return jsonify({'message': 'List medicines API endpoint placeholder'})

@app.route('/api/history')
@login_required
def get_diagnosis_history_api():
    # Your diagnosis history logic here
    # Placeholder response
    return jsonify({'message': 'Diagnosis history API endpoint placeholder'})


if __name__ == '__main__':
    # Ensure tables are created on application startup
    create_tables()
    app.run(debug=True)

