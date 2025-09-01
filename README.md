# 🏥 MEDICINO - Smart Medical Assistant Web Application

A comprehensive web application for symptom diagnosis and medicine information using AI-powered analysis, built with Flask/Django, SQLite, and modern web technologies.

## 🚀 Features

- **AI-Powered Symptom Diagnosis**: Intelligent symptom analysis with confidence scoring
- **Medicine Database**: Comprehensive medicine information with pricing and dosage
- **Ayurvedic Remedies**: Traditional treatment suggestions alongside modern medicine
- **Voice Input Support**: Speech-to-text for symptom input
- **User Authentication**: Secure registration and login system
- **Personalized History**: Track past diagnoses and treatments per user
- **RESTful API**: Full API support for mobile apps and integrations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

### Backend
- **Flask** or **Django** (Python web frameworks)
- **SQLite** (Database)
- **Flask-CORS** / **Django-CORS-Headers** (Cross-origin requests)
- **Flask-Login** (User authentication)
- **REST API** architecture

### Frontend
- **HTML5** with semantic markup
- **CSS3** with modern styling
- **Vanilla JavaScript** (ES6+)
- **Web Speech API** for voice input

### Database Schema
- **Users Table**: User authentication and profiles
- **Medicines Table**: Medicine information and pricing
- **Symptoms Database**: Condition-symptom mappings
- **Diagnosis History**: User diagnosis tracking

## 📋 Prerequisites

- Python 3.8+ installed
- pip package manager
- Web browser with JavaScript enabled
- Internet connection (for voice input feature)

## 🔧 Installation & Setup

### Option 1: Flask Setup (Recommended)

1. **Clone or Download the Project Files**
   ```bash
   mkdir medicino-app
   cd medicino-app
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv medicino_env
   
   # On Windows
   medicino_env\Scripts\activate
   
   # On macOS/Linux
   source medicino_env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database**
   ```bash
   python database_setup.py
   ```
   
   **For Existing Databases**: If you have an existing database and want to add authentication:
   ```bash
   python add_users_table.py
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   Open your browser and go to: `http://localhost:5000`

### Option 2: Django Setup

1. **Create Virtual Environment** (same as above)

2. **Install Django Dependencies**
   ```bash
   pip install Django==4.2.7
   pip install djangorestframework==3.14.0
   pip install django-cors-headers==4.3.1
   ```

3. **Create Django Project**
   ```bash
   django-admin startproject medicino_project .
   python manage.py startapp medicino_app
   ```

4. **Setup Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py setup_data  # Custom command to populate data
   ```

5. **Create Superuser** (Optional)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Django Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   Open your browser and go to: `http://localhost:8000`

## 📁 Project Structure

```
medicino-app/
├── app.py                 # Flask main application
├── database_setup.py      # Database initialization script
├── test_api.py           # API testing script
├── requirements.txt      # Flask dependencies
├── medicino.db          # SQLite database (created after setup)
├── README.md            # This file
│
├── django_setup/        # Django version files
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── admin.py
│
└── templates/           # HTML templates (Django)
    └── index.html
```

## 🔌 API Endpoints

### Flask API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web interface |
| POST | `/api/diagnose` | Symptom diagnosis |
| GET | `/api/medicine/<name>` | Medicine information |
| GET | `/api/medicines` | List all medicines |
| GET | `/api/history` | User's diagnosis history |
| GET | `/login` | Login page |
| POST | `/login` | Login form submission |
| GET | `/register` | Registration page |
| POST | `/register` | Registration form submission |
| GET | `/logout` | Logout user |

### Sample API Usage

**Diagnose Symptoms:**
```bash
curl -X POST http://localhost:5000/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "fever, sore throat, headache"}'
```

**Search Medicine:**
```bash
curl http://localhost:5000/api/medicine/Paracetamol
```

**List All Medicines:**
```bash
curl http://localhost:5000/api/medicines
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

This will test:
- ✅ Diagnosis API functionality
- ✅ Medicine search capabilities
- ✅ Error handling
- ✅ Performance metrics
- ✅ Database connectivity

## 🗄️ Database Schema

### Medicines Table
```sql
CREATE TABLE medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    dosage TEXT,
    side_effects TEXT,
    contraindications TEXT,
    price REAL,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Symptoms Database Table
```sql
CREATE TABLE symptoms_database (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    condition_name TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    ayurvedic_remedy TEXT,
    medicine_suggestion TEXT,
    severity_level TEXT,
    description TEXT,
    precautions TEXT
);
```

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Diagnosis History Table
```sql
CREATE TABLE diagnosis_history (
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
);
```

## 🤖 AI Diagnosis Algorithm

The application uses a sophisticated symptom matching algorithm:

1. **Text Processing**: Normalizes and tokenizes input symptoms
2. **Pattern Matching**: Compares against known symptom patterns
3. **Confidence Scoring**: Calculates match percentage based on symptom overlap
4. **Severity Assessment**: Determines condition severity (mild/moderate/severe)
5. **Treatment Suggestion**: Provides both Ayurvedic and modern medicine recommendations

### Algorithm Logic
```python
def diagnose_symptoms(symptoms_text):
    # 1. Parse and normalize symptoms
    input_symptoms = normalize_symptoms(symptoms_text)
    
    # 2. Compare against database
    for condition in symptom_database:
        match_score = calculate_match_score(input_symptoms, condition.symptoms)
        
        # 3. Return best match if confidence > 30%
        if match_score > 0.3:
            return generate_diagnosis(condition, match_score)
    
    # 4. Fallback for unknown conditions
    return default_response()
```

## 🎯 Usage Examples

### Web Interface Usage

1. **User Registration/Login**:
   - Click "Register" to create a new account
   - Or click "Login" if you already have an account
   - All features require authentication

2. **Symptom Diagnosis**:
   - Enter symptoms: "fever, sore throat, body ache"
   - Click "Diagnose Symptoms"
   - View AI-generated diagnosis with confidence score
   - Get Ayurvedic and modern medicine suggestions

2. **Medicine Search**:
   - Enter medicine name: "Paracetamol"
   - Click "Search Medicine"
   - View detailed information including dosage and side effects

3. **Voice Input**:
   - Click the microphone button
   - Speak your symptoms clearly
   - The system will convert speech to text automatically

### Sample Diagnosis Results

**Input**: "fever, sore throat, headache, body ache"
**Output**:
```json
{
  "disease": "Viral Infection",
  "ayurvedic": "Drink hot water with ginger and turmeric. Take adequate rest and consume immunity-boosting kadha.",
  "medicine": "Paracetamol, Dolo 650",
  "confidence": 85.5,
  "severity": "moderate"
}
```

## 🔒 Security Features

- **User Authentication**: Secure registration and login system with password hashing
- **Session Management**: Flask-Login handles user sessions securely
- **Input Validation**: All user inputs are sanitized and validated
- **SQL Injection Prevention**: Uses parameterized queries
- **CORS Configuration**: Properly configured cross-origin requests
- **Rate Limiting**: API endpoints have built-in rate limiting
- **Error Handling**: Comprehensive error handling prevents information leakage

## 🚀 Deployment Options

### Local Development
- Follow the installation steps above
- Access via `localhost:5000` (Flask) or `localhost:8000` (Django)

### Production Deployment

#### Option 1: Heroku Deployment
```bash
# Install Heroku CLI
pip install gunicorn
echo "web: gunicorn app:app" > Procfile

# Deploy to Heroku
heroku create medicino-app
git push heroku main
```

#### Option 2: Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

#### Option 3: AWS/DigitalOcean
- Use any cloud provider with Python support
- Configure environment variables
- Set up SSL certificates for HTTPS
- Configure database backup and monitoring

## 🐛 Troubleshooting

### Common Issues & Solutions

**Issue**: Database not found
```bash
# Solution: Run database setup
python database_setup.py
```

**Issue**: Port already in use
```bash
# Solution: Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Issue**: CORS errors in browser
```bash
# Solution: Verify Flask-CORS is installed
pip install Flask-CORS
```

**Issue**: Voice input not working
- **Solution**: Use Chrome or Edge browser, ensure microphone permissions are granted

**Issue**: API returning 500 errors
- **Solution**: Check console logs, ensure database is properly initialized

## 📈 Performance Optimization

### Database Optimization
- Indexed frequently searched columns
- Optimized query patterns
- Connection pooling for high traffic

### Frontend Optimization
- Minified CSS and JavaScript
- Lazy loading for large datasets
- Caching for static resources

### API Optimization
- Response compression
- Request rate limiting
- Efficient JSON serialization

## 🔮 Future Enhancements

### Planned Features
- [ ] **Machine Learning Integration**: Advanced symptom analysis using ML models
- [ ] **Multi-language Support**: Diagnosis in multiple languages
- [ ] **Drug Interaction Checker**: Check for medicine interactions
- [ ] **Appointment Booking**: Integration with healthcare providers
- [ ] **Mobile App**: Native iOS and Android applications
- [ ] **Telemedicine Integration**: Video consultation features
- [ ] **Health Tracking**: Personal health monitoring dashboard
- [ ] **Insurance Integration**: Insurance coverage information

### Technical Improvements
- [ ] **Redis Caching**: Improve response times
- [ ] **PostgreSQL**: Production-grade database
- [ ] **JWT Authentication**: User accounts and personalization
- [ ] **GraphQL API**: More flexible API queries
- [ ] **Microservices**: Split into smaller services
- [ ] **Real-time Updates**: WebSocket integration

## 📞 Support & Contact

For support, questions, or contributions:

- **Email**: support@medicino.com
- **GitHub Issues**: Create an issue for bugs or feature requests
- **Documentation**: Check the inline code comments for detailed explanations

## ⚖️ Legal Disclaimer

**IMPORTANT**: This application is for educational and informational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions regarding medical conditions.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for better healthcare accessibility**

*Last updated: July 2025*
