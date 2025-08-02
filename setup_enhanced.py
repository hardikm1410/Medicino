#!/usr/bin/env python3
"""
Enhanced Medicino Setup Script
This script sets up the enhanced Medicino application with all dependencies and database.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    # Check if pip is available
    if not run_command("python -m pip --version", "Checking pip availability"):
        print("❌ pip not available. Please install pip first.")
        return False
    
    # Upgrade pip
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    if not run_command("python -m pip install -r requirements.txt", "Installing requirements"):
        print("❌ Failed to install requirements. Please check requirements.txt")
        return False
    
    return True

def setup_database():
    """Set up the database"""
    print("🗄️  Setting up database...")
    
    try:
        # Import after dependencies are installed
        from app_enhanced import create_app
        from models import db
        
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Check if we need to populate with sample data
            from models import Medicine, Condition
            medicine_count = Medicine.query.count()
            condition_count = Condition.query.count()
            
            if medicine_count == 0 and condition_count == 0:
                print("📝 No data found. Running database setup...")
                if run_command("python database_setup.py", "Populating database with sample data"):
                    print("✅ Database populated successfully")
                else:
                    print("⚠️  Database population failed, but tables are created")
            else:
                print(f"✅ Database already has {medicine_count} medicines and {condition_count} conditions")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_env_file():
    """Create a .env file with default configuration"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Medicino Environment Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///medicino.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    if run_command("python -m pytest tests/ -v", "Running test suite"):
        print("✅ All tests passed")
    else:
        print("⚠️  Some tests failed, but setup can continue")

def show_next_steps():
    """Show next steps for the user"""
    print("\n" + "="*50)
    print("🎉 Enhanced Medicino Setup Complete!")
    print("="*50)
    print("\n📋 Next Steps:")
    print("1. Start the application: python run_enhanced.py")
    print("2. Access the web interface: http://localhost:5000")
    print("3. View API documentation: http://localhost:5000/api/docs")
    print("4. Run tests: python -m pytest tests/")
    print("5. Check the README_ENHANCED.md for detailed documentation")
    print("\n🔧 Development Commands:")
    print("- Run with debug: python run_enhanced.py")
    print("- Run tests: python -m pytest tests/")
    print("- Check coverage: python -m pytest tests/ --cov=.")
    print("- Database migration: python migrate_database.py")
    print("- Verify migration: python migrate_database.py verify")
    print("\n📁 Project Structure:")
    print("- app_enhanced.py: Main application")
    print("- models.py: Database models")
    print("- services.py: Business logic")
    print("- routes/: Route handlers")
    print("- tests/: Test suite")
    print("- config.py: Configuration management")
    print("\n💡 Tips:")
    print("- The application uses SQLAlchemy ORM for database operations")
    print("- All business logic is separated into service classes")
    print("- API endpoints follow RESTful conventions")
    print("- Comprehensive error handling and validation included")
    print("- Security features like password hashing and input sanitization")
    print("\n🚀 Happy coding!")

def main():
    """Main setup function"""
    print("🚀 Enhanced Medicino Setup")
    print("="*30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Setup database
    if not setup_database():
        print("❌ Setup failed at database setup")
        sys.exit(1)
    
    # Run tests
    run_tests()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main() 