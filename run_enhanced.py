#!/usr/bin/env python3
"""
Enhanced Medicino Application Runner
This script provides an easy way to run the enhanced Medicino application.
"""

import os
import sys
from app_enhanced import create_app

def main():
    """Main function to run the enhanced application"""
    print("🚀 Starting Enhanced Medicino Application...")
    
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')
    
    # Create and run the application
    app = create_app()
    
    print("✅ Application created successfully")
    print("🌐 Access the application at: http://localhost:5000")
    print("📚 API Documentation at: http://localhost:5000/api/docs")
    print("🔧 Press CTRL+C to stop the server")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

if __name__ == "__main__":
    main() 